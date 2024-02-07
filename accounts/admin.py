from django.contrib import admin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display=('email','first_name','last_name','contact','address','gender','is_active','is_staff',"created_at")

    fieldsets=((None,{"fields":('email','password','first_name','last_name','contact','address','gender',"created_at")}),
               ("permission",{"fields":('is_staff','is_active')}),
               )
    add_fieldsets=(
        (None,{'classes':("wide",),
               'fields':('email','password','first_name','last_name','contact','address','gender',"created_at",'is_staff','is_active')},
        )
    )
    search_fields=('email',)
    ordering=('email',)

admin.site.register(CustomUser,CustomUserAdmin)