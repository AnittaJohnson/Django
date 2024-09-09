from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SchoolRegistration

class UserAdmin(BaseUserAdmin):
    model = User
    
    list_display = ('email', 'school_name', 'is_active', 'is_admin')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('school_name', 'phone', 'address_area', 'address_landmark', 'address_city',
                                       'address_state', 'address_country', 'address_pincode', 'organization_type')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    list_filter = ('is_admin', 'is_active')
    
    search_fields = ('email', 'school_name')
    
    ordering = ('email',)
    
    filter_horizontal = ()  # Removed filter_horizontal

admin.site.register(User, UserAdmin)
admin.site.register(SchoolRegistration)
