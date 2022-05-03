from django.db import models
from django.contrib.auth.models import User
#models.py how we set up 


# Create your models here.

class Profile(models.Model):
    #user profile; whenever a new user is created 
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=300,blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one entity 
    friends = models.ManyToManyField(User,blank=True, related_name='friends') #many to many field with the user entity 
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}" #return is the username from the user the name of the person 

STATUS_CHOICES = (
    ('sent','sent'),
    ('accepted','accepted')
)

class Relationship(models.Model): #establish the relationship between two profiles 
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender') #a foreign key to the profile class. both associate with the profile class 
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver') 
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="sent")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    

class Post(models.Model): #any post that we create 
    description = models.CharField(max_length=255, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE) #who is making the post 
    image = models.ImageField(upload_to='images',blank=True) #make sure you have pillow installed to show the images 
    date_posted = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.description

class Comment(models.Model): #comment is associated with the post 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE) #who is commenting on the post 
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.text
    
    
class Like(models.Model): #keep track how many likes 
	username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE) 
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)#who liked it and what post they liked it 


