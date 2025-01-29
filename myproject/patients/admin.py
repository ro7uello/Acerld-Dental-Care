from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, Appointment, Profile, PromotionalOffer, Profit


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Profile)
admin.site.register(PromotionalOffer)
admin.site.register(Profit)