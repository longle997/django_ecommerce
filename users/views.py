from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm #, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, now you can sign in!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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