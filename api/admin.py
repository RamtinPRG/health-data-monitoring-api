from django.contrib import admin
from .models import *


"""
This code register models in admin panel with a customized admin view.
"""


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'account_type', 'patient', 'doctor', 'inspector')
    list_filter = ('account_type',)
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('id',)


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ecg', 'body_temp', 'spo2', 'heart_rate')
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('id',)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('id',)


class InspectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)
    search_fields = ('user',)
    ordering = ('id',)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'timestamp', 'status')
    list_filter = ('sender', 'receiver', 'status')
    search_fields = ('sender', 'receiver', 'message')
    ordering = ('id',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Inspector, InspectorAdmin)
admin.site.register(Request, RequestAdmin)
