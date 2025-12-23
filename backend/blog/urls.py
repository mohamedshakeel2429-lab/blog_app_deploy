from django.urls import path
from .import views

app_name='blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('post/<str:slug>',views.details,name="details"),
    path('contact',views.contact,name='contact'),
    path('about',views.aboutus,name='about'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('reset_password/<uidb64>/<token>',views.Reset_password,name='reset_password'),
    path('new_post',views.new_post,name="new_post"),
    path('edit_post/<post_id>',views.edit_post,name="edit_post"),
    path('delete_post/<post_id>',views.delete_post,name="delete_post"),
    path('publish_post/<post_id>',views.publish_post,name="publish_post"),
    path('health',views.health,name='health'),
    
     

]
