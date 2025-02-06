from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Patient, Appointment, PromotionalOffer, Profit, Review


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'patient'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (PatientInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_text', 'created_at')
    search_fields = ('user__username', 'review_text')

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Appointment)
admin.site.register(PromotionalOffer)
admin.site.register(Profit)
admin.site.register(Review, ReviewAdmin)