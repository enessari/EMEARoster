from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Core.models import RosterAudit, RosterUser


@login_required
@csrf_exempt
def myroster_rows(request):
    """
    Obtain all the rows for the connected user is scheduled on.
    """

    # Email address
    email = request.user.email

    # Current year
    year_now = datetime.now().year

    # Variables
    connected_username = ""
    collector = []

    # Get the name of the user based on email from the roster table
    # we not relying on the username that can be obtained via request
    # Since anyone can enter anyname and it will be become hard to
    # manage.
    for user in RosterUser.objects.filter(email=email):
        connected_username = user.first_name + " " + user.last_name

    for audit in RosterAudit.objects.filter(engineer=connected_username).filter(audit_date_field__startswith=year_now).order_by('audit_date_field'):
        collector.append(audit.audit_date_field)

    return JsonResponse(collector, safe=False)
