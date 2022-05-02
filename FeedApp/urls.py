from django.urls import path
from . import views

app_name = 'FeedApp'

urlpatterns = [
    path('', views.index, name='index'),
    #build our profile first, first name,lastname, bio etc 
    path('profile/',views.profile,name='profile'),
    #develop my feed, link at the top of the homepage for all our post 
    #1st work on the profile and then work on my feed 
    path('myfeed',views.myfeed,name='myfeed'),

    
    ]

    