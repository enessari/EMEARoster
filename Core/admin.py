from django.contrib import admin
from .models import RosterAudit, RosterUser


# Audit Roster site display
class RosterUserModelAdmin(admin.ModelAdmin):
    """
    Override the default Django Admin website display and also the response once the employee is added,
    update or deleted ...
    """
    list_display = [
        "first_name",
        "last_name",
        "email",
        "created_at",
        "updated_at",
    ]

    class Meta:
        model = RosterUser


# Audit Roster site display
class RosterAuditsModelAdmin(admin.ModelAdmin):
    """
    Override the default Django Admin website display and also the response once the employee is added,
    update or deleted ...
    """
    list_display = [
        "engineer",
        "audit_date",
        "active",
    ]

    class Meta:
        model = RosterAudit

# Register rest of the models
admin.site.register(RosterUser, RosterUserModelAdmin)
admin.site.register(RosterAudit, RosterAuditsModelAdmin)

