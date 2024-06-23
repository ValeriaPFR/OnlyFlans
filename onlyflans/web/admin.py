from django.contrib import admin
from .models import Client, Flan, ContactForm


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('email', 'name', 'lastname', 'age', 'birth_date', 'address', 'is_active', 'is_staff', 'created_at', 'updated_at', 'get_groups')

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'

admin.site.register(Client, ClientAdmin)

@admin.register(Flan)
class FlanAdmin(admin.ModelAdmin):
    list_display = ('flan_id', 'name', 'description', 'preparation', 'ingredients', 'img_url', 'slug', 'is_private', 'created_at', 'modified_at')

@admin.register(ContactForm)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'message', 'created_at', 'updated_at')
