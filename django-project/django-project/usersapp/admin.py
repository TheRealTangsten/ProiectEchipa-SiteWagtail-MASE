from django.contrib import admin
from .models import user

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ['nume', 'prenume', 'email', 'tip_persoana', 'companie', 'status_cos']
    list_filter = ['tip_persoana', 'status_cos']
    search_fields = ['nume', 'prenume', 'email', 'companie']