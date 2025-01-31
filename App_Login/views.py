from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from App_Login.forms import SignUpForm
from django.contrib.auth.decorators import login_required

# default forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout

def sign_up(request):
    form = SignUpForm()
    registered = False

    # submit korle
    if request.method == 'POST':
        form = SignUpForm(data=request.POST) # save info on form variables

        if form.is_valid():
            form.save()  # db e save hbe
            registered = True

    dict= {'form': form, 'registered': registered}

    return render(request, 'App_Login/signup.html', context= dict)


def login_page(request):
    form = AuthenticationForm()

    if request.method =='POST':
        form = AuthenticationForm(data = request.POST)

        if form.is_valid():
            # default form fields
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # authentication
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)

                # send to another page
                return HttpResponseRedirect(reverse('tasks:task_list'))
            
    return render(request, 'App_Login/login.html',context= {'form':form })


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))



@login_required
def pass_change(request):
    changed = False
    current_user = request.user
    form = PasswordChangeForm(current_user)

    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data= request.POST)

        if form.is_valid():
            form.save()
            changed = True
            logout(request)
            return HttpResponseRedirect(reverse('App_Login:login'))
    
    return render(request, 'App_Login/pass_change.html', context={'form': form, 'changed': changed})

