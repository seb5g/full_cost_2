from importlib import import_module

from copy import deepcopy

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.forms import ValidationError
from django.views import View
from django.db.models import Q, QuerySet
from post_office import mail
from django.core.exceptions import ObjectDoesNotExist
from pathlib import Path

from fullcoster.utils.filter_stuff import filterset_factory_extra
from fullcoster.utils.facturing import generate_xlsx, create_extraction

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import User, Extraction
from .filters import ProjectFilter, ExtractDisplayFilter, ExtractFilterAll, ExtractFilterForm, FilterSet
from .tables import ProjectTable, RecordTableFull, ExtractionTable, RecordTable
from .forms import ExtractionForm


from ..constants.activities import ACTIVITIES, ActivityCategory, get_activities_from_entity
from ..constants.entities import get_entities_as_list, EntityCategory


from ..utils.ldap import LDAP
from ..utils.facturing import calculate_totals
from ..utils.url_stuff import get_field_from_url

from .models import Record, Group

activity_short = Path(__file__).parts[-2]
activity_long = 'CEMES Laboratory'
activity={'short': activity_short, 'long': activity_long}

def get_logged_user(request):
    if not isinstance(request.user, AnonymousUser):
        return f'{request.user.last_name} {request.user.first_name}'
    else:
        return f'Log'

class Index(View):
    activity = activity
    logged = False
    def get(self, request):
        return render(request, 'lab/index.html', {'logged': self.logged,
                                                  'user': get_logged_user(request), 'activity': self.activity, })

class FilterRecord(View):
    extract = False
    thanks = False
    filter_class = None
    table_class = None
    activity = activity

    def get(self, request):
        filter = self.filter_class(request.GET)
        table = self.table_class(filter.qs)
        RequestConfig(request).configure(table)
        return render(request, f"lab/filter_table.html",
                      {'activity': self.activity, 'filter': filter, 'table': table,
                       'export': self.extract, 'thanks': self.thanks, 'user': get_logged_user(request)})

class Projects(View):
    filter_class = ProjectFilter
    table_class = ProjectTable
    activity = activity

    def get(self, request):
        filt = self.filter_class(request.GET)
        table = self.table_class(filt.qs)
        RequestConfig(request).configure(table)
        return render(request, f"lab/filter_table.html",
                      {'activity': self.activity, 'filter': filt, 'table': table, 'user': get_logged_user(request)})

class Export(View):
    table_class = RecordTableFull
    activity = activity

    def get(self, request):
        table = self.table_class(self.table_class._meta.model.objects.all())
        RequestConfig(request).configure(table)
        export_format = "xlsx"
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, table)
            return exporter.response(f"{self.activity['short']}.{export_format}")
        return render(request, f"{self.activity['short']}/filter_table.html",
                      {'activity': self.activity, 'export': True, 'user': get_logged_user(request)})

class GetRecord(View):
    form_class = ModelForm #to subclass by the appropriate class
    record_class = Record
    activity = activity

    def response(self, request, form):
        return render(request, "lab/record.html",
                  {'activity': self.activity, 'form': form, 'user': get_logged_user(request)})

    def validate_record(self, record, form):
        """to be subclassed"""
        validate_state = True
        return form, validate_state #for date range based records: manage_time.check_range_in_range_2_sessions(r, self.record_class, form)

    def populate_record(self, data):
        """to be eventually subclassed"""
        # populate a new record
        #billing field should be populated depending on each activity cases (so in subclasses)
        record = self.record_class()
        for key in data:
            if hasattr(self.record_class, key):
                setattr(record, key, data[key])


        return record

    def check_user(self, data):
        if data['user'].user_last_name == "OTHER":
            user = User(user_first_name=data['user_text_name'].capitalize(),
                        user_last_name=data['user_text_surname'].upper())
            user.save()
            data['user'] = user
        return data

    def get_group(self, user):
        lgroup = None
        ldap = LDAP()
        group = ldap.get_group_ldap(user)
        if group is not None:
            g = Group.objects.filter(group__iexact=group['short'])
            if not g.exists():
                lgroup = Group(group=group['short'].upper(), description=group['long'])
                lgroup.save()
            else:
                lgroup = g[0]
        return lgroup

    def get(self, request):
        user = None
        lgroup = None
        project = None

        if not isinstance(request.user, AnonymousUser):
            user_qs = User.objects.filter(user_last_name__iexact=request.user.last_name)
            if user_qs.exists():
                user = user_qs[0]
                lgroup = user.group
                if lgroup is None:
                    try:
                        lgroup = self.get_group(request.user)
                    except:
                        pass
                    user.group = lgroup
                    user.save()

            else: #add this logged user to the database
                lgroup = self.get_group(request.user)
                u = User(user_last_name=request.user.last_name, user_first_name=request.user.first_name, group = lgroup)
                u.save()


        ini_dict = {'project': project, 'user': user, 'group': lgroup}
        form = self.form_class_init(request, **ini_dict)

        return self.response(request, form)

    def form_class_init(self,request, **kwargs):
        """
        to subclass
        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        return self.form_class(initial=kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data = self.check_user(data)

            if form.is_valid():
                # populate a new record
                record = self.populate_record(data)

                #automatic attribution of the billing entry from ATIVITIES constant

                if record.experiment.exp_type in ACTIVITIES[self.activity['short']]['related_entities']:
                    record.billing = ACTIVITIES[self.activity['short']]['related_entities'][record.experiment.exp_type]

                # check if this record is compatible with existing records or other issue
                form, valid_state = self.validate_record(record, form)

                if form.is_valid() and valid_state:
                    # save it to database
                    record.save()
                    # redirect to a new URL:
                    return HttpResponseRedirect(reverse(f"{self.activity['short']}:thanks"))

        return self.response(request, form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required(f'lab.add_extraction', raise_exception=True), name='dispatch')
class ExtractRecordAll(View):
    filter_class = []
    table_class = RecordTable
    activity = activity


    def extra_filtration_of_records(self, qs):
        """to be subclassed to filter out some records that cannot be extracted, for instance HF2000 for MET"""
        return qs

    def set_filter(self, activities):
        self.filter_class = []
        self.table_class = []
        for act in activities:
            try:
                module = import_module(f"{act}")
                ##self.filter_class.append(deepcopy(ExtractFilterAll))
                self.filter_class.append(filterset_factory_extra(module.models.Record, ('billing', 'date_from', 'project'),FilterSet, ExtractFilterForm))
                self.table_class.append(module.tables.RecordTable)
            except ModuleNotFoundError:
                pass #activity defined in constants.py but not yet as a django app


    def get(self, request):
        entity_previous = None
        url_previous = request.META.get('HTTP_REFERER')
        if url_previous is not None:
            entity_previous =  get_field_from_url(url_previous, 'billing')

        entity = EntityCategory[request.GET.get('billing')]
        full_dates = True
        if entity is None:
            entity = EntityCategory.SPECTRO
        elif entity == entity_previous:
            full_dates = False

        activities = get_activities_from_entity(entity)
        self.set_filter(activities)


        filters = []
        dates_min = []
        dates_max = []
        for ind, filter in enumerate(self.filter_class):
            filters.append(filter(request.GET))

            if full_dates:
                module = import_module(f"{activities[ind].name}")
                sub_billings = [entity]
                req = Q()
                for sub in sub_billings:
                    req = req | Q(experiment__exp_type=sub)
                qs = module.models.Record.objects.filter(req, extraction=None, )
                if qs.exists():
                    dates_min.append(qs.earliest('date_from').date_from)
                    dates_max.append(qs.latest('date_from').date_from)

        if full_dates and dates_min != []:
            filters = []
            date_min = min(dates_min)
            date_max = max(dates_max)
            for filter in self.filter_class:
                filters.append(filter(data={'billing': entity, 'date_from_after': date_min, 'date_from_before': date_max}, request=request.GET))

        filter = filters[0]

        tables = []
        qss = []
        for ind, filter in enumerate(filters):
            sub_billings = (entity,)
            req = Q()
            for sub in sub_billings:
                req = req | Q(experiment__exp_type=sub)
            qs = filter.qs.filter(req, extraction=None, )
            # if not qs.exists():
            #     filters[0].form.add_error('project', ValidationError(('No records to extract'), code='project_error'))
            tables.append(self.table_class[ind](qs))
            qss.append(qs)
            RequestConfig(request).configure(tables[-1])

        export = False
        amount = -1
        if filter.form.is_valid() and len(request.GET) != 0:
            if 'project' not in request.GET:
                filter.form.add_error('project', ValidationError(('Pick one project to extract from'), code='project_error'))
            elif request.GET['project'] == '':
                filter.form.add_error('project', ValidationError(('Pick one project to extract from'), code='project_error'))
            if 'date_from_before' not in request.GET:
                filter.form.add_error('date_from', ValidationError(('Select dates to extract from'), code='date_error'))
            elif request.GET['date_from_before'] == '':
                filter.form.add_error('date_from', ValidationError(('Select dates to extract from'), code='date_error'))

            if 'date_from_after' not in request.GET:
                filter.form.add_error('date_from', ValidationError(('Select dates to extract from'), code='date_error'))
            elif request.GET['date_from_after'] == '':
                filter.form.add_error('date_from', ValidationError(('Select dates to extract from'), code='date_error'))

            if filter.form.is_valid():
                project = filter.form.cleaned_data['project']
                export = True
                amount = calculate_totals(project, qss, entity)[0]

                if '_export' in request.GET:
                    ext = create_extraction(entity, qss, project, filter)
                    return redirect('lab:fextract_entity_id', entity=entity, id=ext.creation_id, thanks='true')


        return render(request, f"{self.activity['short']}/filter_table_lab.html",
                    {'activity': self.activity, 'filter': filter, 'tables':tables, 'activities': activities,
                     'export':export, 'user': f'{request.user.last_name} {request.user.first_name}', 'amount': amount})

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required(f'lab.view_extraction', raise_exception=True), name='dispatch')
class ShowSetExtractionAll(View):
    form_class = ExtractionForm
    filter_class = ExtractDisplayFilter
    table_class = ExtractionTable
    activity = activity

    def response(self, request, table, form, filter, thanks='', ext=None, email_status=True):
        if thanks == '':
            thanks = False
        else:
            thanks = True
        modification = request.user.has_perm('lab.change_extraction')
        if ext is not None:
            submitting = request.user.has_perm('lab.delete_extraction') and not ext.submitted
        else:
            submitting = request.user.has_perm('lab.delete_extraction')
        return render(request, "lab/filtered_extractions.html",
                      {'activity': self.activity, 'filter': filter, 'table': table, 'form': form,
                       'thanks': thanks, 'modification': modification, 'submitting': submitting,
                       'user': f'{request.user.last_name} {request.user.first_name}',
                       'email_status': email_status})


    def set_as_factured(self, ext, factured=True):
        if ext.factured != factured:
            ext.factured = factured
            ext.save()
            p = ext.project
            if factured:
                p.amount_left -= ext.amount
            else:
                p.amount_left += ext.amount
            p.save()

    def delete(self, ext):
        if ext.factured:
            self.set_as_factured(ext, False)
        ext.delete()

    def submit(self, ext, user):
        """
        Extraction(project=project,
                     date_after=filter.form.cleaned_data['date_from'].start,
                     date_before=filter.form.cleaned_data['date_from'].stop,
                     creation_id=ext_id, amount=total, billing=entity)

        """
        #get pi email
        project = ext.project
        pi = ext.project.project_pi
        ldap = LDAP()
        try:
            email_pi = ldap.get_user_info_last_name(pi.user_last_name)['mail'][0].decode()
        except:
            email_pi = 'unknown.pi@cemes.fr'
        ext.submitted = True
        ext.save()

        try:
            # send email to admin
            mail.send(['fullcost@new-sympa.cemes.fr', email_pi],
                      email_pi,
                      subject='FULL cost: An extraction has been submitted',
                      message=(f'Hello,\nThe extraction {ext.billing}-{ext.creation_id:03d} has been made on the project: '
                               f'{ext.project} by {user.last_name} {user.first_name}.\n'
                               f'The PI of this project is {pi} belonging to the {pi.group} group\n'
                               f'Please log in to process it:\n'
                               f'http://full-cost.cemes.fr/lab/fextractions/\n'
                               f'Thanks\n\nThe full cost administrator!'

                               ),
                      priority='now',
                      )
            return True
        except:
            return False

    def post(self, request, entity=None, id=-1, thanks=''):
        form = self.form_class(request.POST)
        status = True
        if form.is_valid():
            ext = form.cleaned_data['extractions']
            if 'factured' in request.POST:
                self.set_as_factured(ext, factured=True)

            elif 'unfactured' in request.POST:
                self.set_as_factured(ext, factured=False)

            elif 'download' in request.POST:
                response = generate_xlsx(ext)
                return response

            elif 'delete' in request.POST:
                self.delete(ext)

            elif 'submit' in request.POST:
                status = self.submit(ext, request.user)

        filter = self.filter_class(request.GET)  # get all objects from the filter model
        table = self.table_class(filter.qs)
        RequestConfig(request).configure(table)

        return self.response(request, table, form, filter, ext=ext, email_status=status)

    def get(self, request, entity=None, id=-1, thanks=''):
        filter = self.filter_class(request.GET)  # get all objects from the filter model

        table = self.table_class(filter.qs)
        RequestConfig(request).configure(table)
        if entity is not None and id != -1:
            ext = Extraction.objects.filter(creation_id=id, billing=entity)
            if ext.exists():
                form =self.form_class(initial={'extractions' : ext[0]})
            else:
                form = self.form_class()
        else:
            form = self.form_class()


        return self.response(request, table, form, filter, thanks)

class LoadExperiments(View):
    """view used to modify dynamically the content of the field experiment in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    def set_experiments(self, request):
        """to subclass"""
        experiments = QuerySet()
        return experiments

    def get(self, request):
        experiments = self.set_experiments(request)
        return render(request, 'lab/experiments.html', {'experiments': experiments})

class LoadSessions(View):
    """view used to modify dynamically the content of the field time_to or time_from in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    def set_sessions(self, request):
        """to subclass"""
        sessions = QuerySet()
        return sessions

    def get(self, request):
        sessions = self.set_sessions(request)
        return render(request, 'lab/sessions.html', {'sessions': sessions})

class LoadHTMLData(View):
    """view used to modify dynamically the content of a given field in the record form.
     The ajax call to this view is configured within the dedicated javascript file, see static"""
    template = 'lab/subhtml.html'

    def set_values(self, request):
        """to subclass"""
        values = QuerySet()
        return values

    def get(self, request):
        values = self.set_values(request)
        return render(request, self.template, {'values': values})