from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.views.generic import FormView

from accounts.forms import OTPForm
from accounts.utils import generate_otp, send_otp


class SendOTPView(FormView):
    """Get user's phone number and send OTP. """

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        otp = generate_otp()
        self.request.session['phone'] = phone
        self.request.session['otp'] = otp
        self.request.session.set_expiry(settings.OTP_EXPIRATION_TIME)
        send_otp(otp, phone)
        response = redirect(self.success_url)
        response.set_cookie('sessionid', self.request.session.session_key)
        return response

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)


class VerifyOTPView(FormView):
    form_class = OTPForm
    model = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_model(self):
        if self.model is None:
            raise ImproperlyConfigured("Please set `model` attribute.")
        return self.model

    def form_valid(self, form):
        phone = self.request.session.get('phone')
        # This part is common between Register and Login. In Login situation we get and in the
        # Register situation we create the user based on the `model` attribute.
        user, created = self.get_model().objects.get_or_create(phone=phone)

        self.request.session.delete()
        login(self.request, user)
        messages.success(self.request, f"شما با موفقیت وارد شدید `{phone}`")

        return super().form_valid(form)

    def form_invalid(self, form):
        for error, message in form.errors.items():
            messages.error(self.request, message)
        return super().form_invalid(form)
