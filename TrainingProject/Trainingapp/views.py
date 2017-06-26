from django.shortcuts import render
from Trainingapp.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'Trainingapp/index.html')

@login_required
def special(request):

    LOGIN_URL = '/Trainingapp/user_login/'
    return HttpResponse("You are logged in. Great Job!")

@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Saving User Form to Database
            user = user_form.save()

            # Hash the password(implemented hashing)
            user.set_password(user.password)

            # Update with Hashed password
            user.save()




            profile = profile_form.save(commit=False)


            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')

                profile.profile_pic = request.FILES['profile_pic']

            # saving model
            profile.save()

            # Registration Successful!
            registered = True

        else:

            print(user_form.errors,profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'Trainingapp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)


        if user:
            #Check if the account is active
            if user.is_active:

                login(request,user)

                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'Trainingapp/login.html', {})
