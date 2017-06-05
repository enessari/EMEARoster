import logging
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout


logger = logging.getLogger('roster')
logging.basicConfig(format='%(asctime)s:[%(levelname)s]: %(message)s', level=logging.INFO)


def Login(request):
    """
    User Login method
    """
    logging.info("Redirecting to login page...")
    return render(request, 'Core/login.html')


def Logout(request):
    """
    User Logout method
    """
    logging.info("Request to logout from roster...")
    logout(request)
    return HttpResponseRedirect('/login')
