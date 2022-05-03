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

@login_required
def myfeed(request):
    comment_count_list = []
    like_count_list = [] 
    #we have multiple posts, so we would like to have comment and likes for each post 
    #went back to the models.py to check what's in the post
    posts = Post.objects.filter(username = request.user).order_by('-date_posted') #- means it's the reverse order
    #we would like to order then in the reverse order, the newest show on the top 
    #we would like to iterate through loop 
    for p in posts: 
        c_count = Comment.objects.filter(post=p).count()
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
        #zip it all up, so we can iterate all together 
    zipped_list = zip(posts,comment_count_list,like_count_list)

    context = {'posts':posts,"zipped_list":zipped_list}
    return render(request, 'FeedApp/myfeed.html',context)

#create a post within myfeed including different functionality 
@login_required
def new_post(request):
    #see if it's get or post 
    #get - load an empty form 
    #post request - save to the database 
    if request.method != 'POST':
        #just load the blank form 
        form = PostForm()
    else:
        #process it into the database, getting everything from the website, and save the image 
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():#if the form is valid, we need to attach the username to it 
            #date will be automatically add to it in the models.py file 
            #but we do need to add the username to it 
            new_post = form.save(commit=False) #we're not commit it to the database yet 
            new_post.username = request.user #now we are getting the user name 
            new_post.save()
            return redirect('FeedApp:myfeed') #keep them at the same location so they can see 
    
    context = {'form':form}
    return render(request,'FeedApp/new_post.html',context)

#develop the function or the comments 
@login_required
def comments(request,post_id):
    #we want to see if someone click the button for the comment 
    #once they do, we will know what do to with the comment button 
    #comment will be a link and someone click on it - redirect to another page to leave a comment 

    #to check if the request is post and also we want to see if the submit button is clicked 
    if request.method == 'POST' and request.POST.get("btn1"):
        comment = request.POST.get("comment")
        #make a new row - capital because it's in the model, in the comment model 
        Comment.objects.create(post_id=post_id,username=request.user,text=comment,date_added=date.today())
    
    #we want to refresh and let the comment show up 
    comments= Comment.objects.filter(post=post_id)
    post = Post.objects.get(id=post_id)

    context = {'post':post,'comments':comments}
    return render(request, 'FeedApp/comments.html',context)


#friends feed
@login_required
def friendsfeed(request):
    comment_count_list = []
    like_count_list = [] 
    friends = Profile.objects.filter(username = request.user).values('friends')
    posts = Post.objects.filter(username = request.user).order_by('-date_posted')

    for p in posts: 
        c_count = Comment.objects.filter(post=p).count()
        l_count = Like.objects.filter(post=p).count()
        comment_count_list.append(c_count)
        like_count_list.append(l_count)
    zipped_list = zip(posts,comment_count_list,like_count_list)

    #if the form is submitted and the submitted button is pressed 
    if request.method =='POST' and request.POST.get("like"):
        post_to_like = request.POST.get("like")
        print(post_to_like)
        #make sure they won't like again 
        like_already_exists = Like.objects.filter(post_if=post_to_like,username=request.user)
        #check in the models.py 
        if not like_already_exists():
            Like.objects.create(post_id=post_to_like,username=request.user)
            return redirect("FeedApp:friendsfeed")


    context = {'posts':posts,"zipped_list":zipped_list}
    return render(request, 'FeedApp/friendsfeed.html',context)