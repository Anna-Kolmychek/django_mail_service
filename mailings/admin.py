from django.contrib import admin

from mailings.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sending_time_start', 'sending_time_end', 'periodicity', 'status', 'mail_title', 'pk', ]
    list_filter = ['periodicity', 'status',]
    search_fields = ['title', 'description', 'mail_title', 'mail_content']

