import jdatetime
from django import template
from django.utils import timezone

register = template.Library()
jdatetime.set_locale("fa_IR")
FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


@register.filter
def jdate(value):
    """۱۴۰۵/۰۸/۱۰ شنبه → «شنبه ۱۰ آبان»"""
    if not value:
        return ""
    j = jdatetime.datetime.fromgregorian(datetime=timezone.localtime(value))
    return j.strftime("%A %d %B").translate(FA)


@register.filter
def jtime(value):
    if not value:
        return ""
    return timezone.localtime(value).strftime("%H:%M").translate(FA)


@register.filter
def fa_money(value):
    if value in (None, ""):
        return ""
    return f"{int(value):,}".replace(",", "٬").translate(FA)
