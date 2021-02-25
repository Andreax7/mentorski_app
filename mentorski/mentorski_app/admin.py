from django.contrib import admin
from .models import Korisnici, Predmeti, Upisi
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class KorisniciAdmin(UserAdmin):
    pass
admin.site.register(Korisnici, KorisniciAdmin)

class PredmetiAdmin(admin.ModelAdmin):
    pass
admin.site.register(Predmeti, PredmetiAdmin)

class UpisiAdmin(admin.ModelAdmin):
    pass
admin.site.register(Upisi, UpisiAdmin)