from django.contrib import admin
from .models import Contact
from .models import Quote
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'Subject', 'created_at')
    search_fields = ('name', 'email', 'Subject')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
