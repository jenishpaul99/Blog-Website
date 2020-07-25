from django.shortcuts import render,redirect
from .forms import NewUserCreationForm,EmailUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=='POST':
        form=NewUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')       
            messages.success(request,f'Account created for {username}')
            return redirect('login')
    else:
        form = NewUserCreationForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        userForm=EmailUpdateForm(request.POST,instance=request.user)
        profileForm=ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            messages.success(request,'Your Profile has been Updated')
            return redirect('profile')
    else:        
        userForm=EmailUpdateForm(instance=request.user)
        profileForm=ProfileUpdateForm(instance=request.user.profile)
    
    data={'userForm':userForm,'profileForm':profileForm}
    return render(request,'users/profile.html',data)
