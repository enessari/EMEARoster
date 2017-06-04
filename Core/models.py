from django.db import models


class RosterUser(models.Model):
    """
    Table: RosterUser
    Comment: Table that stores all users of roster.
    """
    first_name = models.CharField(db_index=True, max_length=100, null=False)
    last_name = models.CharField(db_index=True, max_length=100, null=False)
    email = models.EmailField(db_index=True, max_length=100, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.email


class RosterAudit(models.Model):
    """
    Table: RosterAudits
    Comment: Table that stores all the changes in schedule of the engineer.
    """
    engineer = models.CharField(db_index=True, max_length=100, null=False)
    audit_date = models.CharField(db_index=True, max_length=20, null=False)
    audit_date_field = models.DateField(db_index=True, null=False)
    active = models.BooleanField(db_index=True, null=False, default=True)

    def __str__(self):
        return self.engineer + "-" + self.audit_date[5:]