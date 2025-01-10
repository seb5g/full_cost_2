from django_filters.constants import ALL_FIELDS
from django_filters.filterset import FilterSet
from django import forms

def filterset_factory_extra(model, fields=ALL_FIELDS, filterset_extra=FilterSet, form=forms.Form):
    meta = type(str('Meta'), (object,), {'model': model, 'fields': fields, 'form':form})
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                     (filterset_extra,), {'Meta': meta})
    return filterset