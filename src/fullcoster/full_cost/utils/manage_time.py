from datetime import date, datetime
import portion as inter
import math
import numpy as np
from django.db.models import Q
from django.forms import ValidationError

dates_error = ValidationError(('Chosen dates for this experiment are already used'),
                                                         code='invalid_dates')
date_error = ValidationError(('Chosen date for this experiment is already used'),
                                                         code='invalid_date')
time_error = ValidationError(('Chosen time for this experiment is already used'),
                                                         code='invalid_date')


def elapsed_days(d1, d2):
    if not (isinstance(d1, date) or isinstance(d1, datetime)) or \
       not (isinstance(d2, date) or isinstance(d2, datetime)):
        raise TypeError('Days should be datetime.date or datetime.datetime objects')
    return abs(d2-d1).days

def elapsed_weekdays(d1, d2):
    if not (isinstance(d1, date) or isinstance(d1, datetime)) or \
       not (isinstance(d2, date) or isinstance(d2, datetime)):
        raise TypeError('Days should be datetime.date or datetime.datetime objects')

    if isinstance(d1, datetime):
        d1 = d1.date()
    if isinstance(d2, datetime):
        d2 = d2.date()

    return abs(np.busday_count(d1, d2))


def elapsed_hours(d1,d2):
    if not (isinstance(d1, date) or isinstance(d1, datetime)) or \
       not (isinstance(d2, date) or isinstance(d2, datetime)):
        raise TypeError('Days should be datetime.date or datetime.datetime objects')
    return math.floor(abs(d2 - d1).total_seconds()/3600)

def elapsed_hours_weekdays(d1, d2):
    if not (isinstance(d1, date) or isinstance(d1, datetime)) or \
       not (isinstance(d2, date) or isinstance(d2, datetime)):
        raise TypeError('Days should be datetime.date or datetime.datetime objects')
    if not isinstance(d1, datetime):
        d1 = datetime(d1)
    if not isinstance(d2, datetime):
        d2 = datetime(d2)
    hours = abs(d2-d1).seconds // 3600
    hours += elapsed_weekdays(d1, d2) * 24
    return hours

def is_range_intersecting_datetime(record, Record):
    error = None
    r_exp = Record.objects.filter(experiment__exact=record.experiment)
    for ind, r in enumerate(r_exp):
        inter1 = inter.closed(datetime.combine(record.date_from, record.time_from),
                              datetime.combine(record.date_to, record.time_to))
        inter2 = inter.closed(datetime.combine(r.date_from, r.time_from),
                              datetime.combine(r.date_to, r.time_to))
        date_inter = inter1 & inter2
        if not date_inter.empty:
            if not date_inter.lower == date_inter.upper:  # could be an intersection within or on the edges which is
                # fine as it represents the same seconds or microseconds
                error = dates_error
                break

    return error



def is_range_intersecting_date_session(record, Record):
    error = None
    r_exp = Record.objects.filter(experiment__exact=record.experiment)
    for ind, r in enumerate(r_exp):
        inter1 = inter.closed(record.date_from, record.date_to)
        inter2 = inter.closed(r.date_from, r.date_to)
        date_inter = inter1 & inter2
        if not date_inter.empty:
            if date_inter.lower == date_inter.upper: #could be an intersection within or on the edges
                # check if it is on the edges:
                if inter1 <= inter2 or inter1 >= inter2:
                    #check if sessions/times overlapp
                    error =is_range_intersecting_session(record, [r])
                    time_inter = inter.closed(record.time_from, record.time_to) & inter.closed(r.time_from, r.time_to)
                    if not time_inter.empty:
                        error = time_error
                        break
                else:
                    error = dates_error
                    break

            else:
                error = dates_error
                break
    return error


def is_range_intersecting_session(record, records):
    error = None
    for ind, r in enumerate(records):
        #check if sessions/times overlapp
        time_inter = inter.closed(record.time_from, record.time_to) & inter.closed(r.time_from, r.time_to)
        if not time_inter.empty:
            error = time_error
            break

    return error

def is_date_in_date(record, records):
    error = None
    for ind, r in enumerate(records):
        if r.date_from == record.date_from:
            error = time_error
            break

    return error