from django.shortcuts import render, redirect
from .forms import PostForm,ProfileForm, RelationshipForm
from .models import Post, Comment, Like, Profile, Relationship
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

# When a URL request matches the pattern we just defined, 
# Django looks for a function called index() in the views.py file. 

def index(request):
    """The home page for Learning Log."""
    return render(request, 'FeedApp/index.html')
    #home page 




@login_required #decorator, authentication decorator; 
def profile(request): #posting to the webpage and getting things from the webpage to the database 
    #after they login they can see the profile 
    profile = Profile.objects.filter(user=request.user) #currently log in to the system; check if this user have a profile or not 
    #get does not work with exist but filter does 
    if not profile.exists(): #if doesnot exist 
        Profile.objects.create(user=request.user)
    profile = Profile.objects.get(user=request.user) #now, we have the user exist, and we can grab the profile now 

    if request.method != 'POST': #if the request is not equal to post. load the webpage 
        #forms.py already create the form for us  
        form = ProfileForm(instance=profile) #the form will be the profile form, load not a blank form 
    else:
        form = ProfileForm(instance=profile,data=request.POST) #is post, we are trying to save it to the database. the data coming in from the webpage is what we are going to save 
        if form.is_valid(): #to check and see if the form is valid 
            form.save() #if the form is valid, we just save it 
            return redirect('FeedApp:profile') #redirect to the profile page 
    

    context = {'form':form} #we want to make sure it's not indented 
    return render(request,'FeedApp/profile.html',context) 


