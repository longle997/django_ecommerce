import random
import string
import redis

from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# we import the settings object which contains all the global
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from .forms import UserRegisterForm, UserActivateForm #, ProfileUpdateForm
from store.models import CustomUser as User


def random_string():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))

redis_instance = redis.StrictRedis(
    settings.REDIS_HOST,
    settings.REDIS_PORT,
    0,
    )


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            activation_code = random_string()
            context = {'title': 'Activation Email', 'code': activation_code}
            # define a template for sending email
            msg_html = render_to_string('users/active_account_email.html', context=context)
            try:
                send_mail(
                    # subject and message params cannot be leave blank
                    subject='',
                    message='',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                    fail_silently=False,
                    html_message=msg_html
                )
                # 600 is for ex(experation time for cache) parameter
                redis_instance.set(user_email, activation_code, 600)
            except:
                return HttpResponseBadRequest('email was used for register is invalid, please try another one!')
            messages.success(request, f'Account created for {username}, now you can sign in!')
            return redirect('validate_email')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def validate_email(request):
    if request.method == 'POST':
        form = UserActivateForm(request.POST)
        if form.is_valid:
            user_email = form.data.get('email')
            activation_code = form.data.get('activation_code')
            try:
                cache_result = redis_instance.get(user_email)
                if cache_result.decode() == activation_code:
                    user_object = User.objects.get(email = user_email)
                    user_object.is_email_valid = True
                    user_object.save()
                    return redirect('login')
                else:
                    # raise ValidationError(
                    #     ('Can not verify user email: %(value)s'),
                    #     params={'value': user_email},
                    # )
                    return render(request, 'users/verify_email.html', {'message':f'Can not verify user email: {user_email} with activation code: {activation_code}', 'form': form})

            except:
                # raise ValidationError(
                #     ('Can not verify user email: %(value)s'),
                #     params={'value': user_email},
                # )
                return render(request, 'users/verify_email.html', {'message':f'Can not verify user email: {user_email} with activation code: {activation_code}', 'form': form})
    else:
        form = UserActivateForm()
    return render(request, 'users/verify_email.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         # to let program know that which user you wanna update
#         # you need to pass update form function it's instance
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         # Because addition data (image) will comming with the request
#         # So we need to clarify
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid():
#             u_form.save()
#             messages.success(request, f'Your profile was updated successfully')
#             # we need to redirect because we don't wanna go to render function with POST method
#             # that will cause error. By redirect, we'll go to profile page with GET method
#             return redirect('profile')
#         elif p_form.is_valid():
#             p_form.save()
#             messages.success(request, f'Your profile was updated successfully')
#             return redirect('profile')
#         else:
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     # we'll pass this dictionary to render function and we can access this dic inside tenplate
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }

#     return render(request, 'users/profile.html', context)