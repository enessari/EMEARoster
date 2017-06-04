import logging, json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from data_engine.scheduler import Scheduler
from data_engine.shuffler import Shuffler
from data_engine.lib import save_shuffle_schedule, get_audit_rows, delete_audits_by_dates, update_audit_table
from data_engine.lib import delete_audit_rows


logger = logging.getLogger('roster')
logging.basicConfig(format='%(asctime)s:[%(levelname)s]: %(message)s', level=logging.INFO)


# Create your views here.
@login_required
def index(request):
    """
    Main method that is called and populate the roster schedule.
    """

    logging.info("Requesting data from data engine roster to provide JSON data to scheduler.html...")
    return render(request, 'Scheduler/scheduler.html')


@login_required
@csrf_exempt
def get_rows(request):
    """
    Get rows for the roster.
    """
    logging.info("Getting rows for the roster...")

    # If the request is of POST Method.
    if request.method == "POST":
        new_search_date = dict(request.POST.iterlists())
        from_date = new_search_date['from_date'][0]
        to_date = new_search_date['to_date'][0]
        return JsonResponse(Scheduler(from_date, to_date).get_rows(), safe=False)

    # If its a get request
    else:
        return JsonResponse(Scheduler().get_rows(), safe=False)


@login_required
@csrf_exempt
def shuffle_rows(request):
    """
    Return Shuffle rows
    """

    logging.info("providing shuffle rows")

    # If the request is of POST Method.
    if request.method == "POST":
        new_search_date = dict(request.POST.iterlists())
        from_date = new_search_date['from_date'][0]
        to_date = new_search_date['to_date'][0]
        return JsonResponse(Shuffler(from_date, to_date).shuffle(), safe=False)

    # If its a get request, redirect to main home page
    else:
        return redirect("/")


@login_required
@csrf_exempt
def shuffle_save(request):
    """
    Save the shuffle rows
    """

    logging.info("Saving shuffled rows")

    # If the request is of POST Method.
    if request.method == "POST":
        saved_rows = dict(request.POST.iterlists())
        save_shuffle_schedule(saved_rows)
        return HttpResponse('success')

    # If its a get request, redirect to main home page
    else:
        return redirect("/")


@login_required
@csrf_exempt
def send_audit_rows(request):
    """
    Send Audit Rows
    """
    logging.info("sending audit rows")

    # If the request is of POST Method.
    if request.method == "POST":
        new_search_date = dict(request.POST.iterlists())
        from_date = new_search_date['from_date'][0]
        to_date = new_search_date['to_date'][0]
        return JsonResponse(get_audit_rows(from_date, to_date), safe=False)

    # If its a get request, redirect to main home page
    else:
        return redirect("/")


@login_required
@csrf_exempt
def delete_date_rows(request):
    """
    Delete Audit Rows based on dates
    """

    logging.info("Deleting audits rows by dates")

    # If the request is of POST Method.
    if request.method == "POST":
        new_search_date = dict(request.POST.iterlists())
        from_date = new_search_date['from_date'][0]
        to_date = new_search_date['to_date'][0]
        return JsonResponse(delete_audits_by_dates(from_date, to_date), safe=False)

    # If its a get request, redirect to main home page
    else:
        return redirect("/")


@login_required
@csrf_exempt
def updatecell(request):
    """
    Update the cell
    """

    logging.info("Update the cell for his/her availability")
    # If Database was successful in updating
    try:
        # If the request is of POST Method.
        if request.method == "POST":
            post_dict = dict(request.POST.iterlists())
            post_keys = json.loads(post_dict.keys()[0])['key']
            post_what_to_do = json.loads(post_dict.keys()[0])['what_to_do']

            if post_what_to_do == "update":
                update_audit_table(post_keys)
            elif post_what_to_do == "delete":
                delete_audit_rows(post_keys)

            return HttpResponse("success")

        # If its a get request, redirect to main home page
        else:
            return redirect("/")

    # If Database failed in updating
    except Exception as e:

        # Send the error message as response for troubleshooting
        return HttpResponse(e)
