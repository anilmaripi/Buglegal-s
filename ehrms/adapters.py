import logging
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from datetime import datetime
import pytz
from ehrms.models import CustomUser, Companys, Employs, freetraildays


logger = logging.getLogger(__name__)
User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        if hasattr(user, 'socialaccount'):
            logger.debug(f"User {user.email} is logging in with a social account.")
            return None
        else:
            logger.debug(f"User {user.email} is signing up through other means.")
            return super().save_user(request, user, form, commit)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        extra_data = sociallogin.account.extra_data
        email = extra_data.get('email')
        request.session['email'] = email
        request.session['username'] = extra_data.get('given_name')
        process = request.GET.get('process', sociallogin.state.get('process', 'login'))
        oldpath = sociallogin.state.get('next')
        request.session['oldpath'] = oldpath

        logger.debug(f"Pre-social login for email: {email}, process: {process}")

        if email:
            try:
                user = User.objects.get(email=email)
                if process == 'login':
                    if sociallogin.is_existing:
                        user = sociallogin.account.user
                    else:
                        sociallogin.connect(request, user)

                    backend = 'allauth.account.auth_backends.AuthenticationBackend'
                    request.session['socialaccount_user'] = user.id
                    request.session['socialaccount_backend'] = backend
                    logger.debug(f"User {email} exists and is being logged in.")
                    raise ImmediateHttpResponse(redirect('/social_login_complete/'))
                elif process == 'signup':
                    request.session['sociallogin'] = sociallogin.serialize()
                    backend = 'allauth.account.auth_backends.AuthenticationBackend'
                    request.session['socialaccount_backend'] = backend
                    logger.debug("Process is signup. Redirecting to company form.")
                    raise ImmediateHttpResponse(HttpResponseRedirect('/company-form/'))
                else:
                    logger.debug("Invalid process specified. Raising exception.")
                    raise ImmediateHttpResponse(HttpResponseBadRequest('Invalid process specified.'))
            except User.DoesNotExist:
                if process == 'signup':
                    logger.debug("Process is signup and user does not exist. Redirecting to company form.")
                    request.session['sociallogin'] = sociallogin.serialize()
                    backend = 'allauth.account.auth_backends.AuthenticationBackend'
                    request.session['socialaccount_backend'] = backend
                    raise ImmediateHttpResponse(HttpResponseRedirect('/company-form/'))
                else:
                    logger.debug(f"User with email {email} does not exist. Raising exception.")
                    messages.error(request, "You don't have an account.")
                    raise ImmediateHttpResponse(redirect('/show_login/'))
        else:
            logger.debug("Email not provided. Raising exception.")
            raise ImmediateHttpResponse(HttpResponseBadRequest('Email not provided.'))

def social_login_complete(request):
    user_id = request.session.get('socialaccount_user')
    backend = request.session.get('socialaccount_backend')
    logger.debug(f"Social login complete for user_id: {user_id}, backend: {backend}")
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            # Specify the authentication backend when logging in the user
            login(request, user, backend=backend)
            return redirect_authenticated_user(request, user)
        except User.DoesNotExist:
            logger.error(f"User with id {user_id} not found.")
            messages.error(request, "User not found")
    else:
        logger.error("User ID not found in session.")
        messages.error(request, "Social login error")
    return redirect('/show_login')

def redirect_authenticated_user(request, user):
    logger.debug(f"Redirecting authenticated user: {user.email}")
    if user.is_superuser:
        return HttpResponseRedirect("/adminAdashboard/")

    companys = None
    loginemploy = None

    try:
        companys = Companys.objects.filter(usernumber=user).first()
        logger.debug(f"Companys record found: {companys}")
    except Companys.DoesNotExist:
        logger.debug(f"No Companys record found for user: {user.email}")

    try:
        loginemploy = Employs.objects.filter(admin=user).first()
        logger.debug(f"Employs record found: {loginemploy}")
    except Employs.DoesNotExist:
        logger.debug(f"No Employs record found for user: {user.email}")

    compid = None
    freetraile = None
    plandate = None

    if loginemploy:
        compid = loginemploy.companyid
    if companys:
        freetraile = companys.freetraile
        plandate = companys.date
    elif compid:
        freetraile = compid.freetraile
        plandate = compid.date 

    current_date = datetime.now(pytz.utc)
    if plandate:
        plandate = datetime.combine(plandate, datetime.min.time()).replace(tzinfo=pytz.utc)
        logger.debug(f"Plan date: {plandate}")

    free = freetraildays.objects.first()
    
    if plandate:
        days_since_plan = (current_date - plandate).days
        logger.debug(f"Days since plan start: {days_since_plan}")
        if freetraile == 1 and days_since_plan > free.freedays:
            messages.error(request, "Your Free Trial Expired")
            return HttpResponseRedirect("/show_login")
        elif freetraile == 0 and days_since_plan > free.monthly:
            messages.error(request, "Your Plan Expired")
            return HttpResponseRedirect("/show_login")
        elif freetraile == 2 and days_since_plan > free.yearly:
            messages.error(request, "Your Plan Expired")
            return HttpResponseRedirect("/show_login")

    if user.user_type == "2":
        user.save_login_record()
        if compid:
            return HttpResponseRedirect(reverse("Employ_home"))
        else:
            return HttpResponseRedirect("/show_login")

    if user.user_type == "1":
        if companys:
            return HttpResponseRedirect('/admin_home')
        else:
            return HttpResponseRedirect("/show_login")

    if user.user_type == "0":
        messages.error(request, "You have been disabled")
        return HttpResponseRedirect("/show_login")

    return HttpResponseRedirect("/show_login")

   
      
    
