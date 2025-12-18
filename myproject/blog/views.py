from django.shortcuts import get_object_or_404
from blog.forms import PostForm
from blog.models import Category
from django.shortcuts import render,redirect
import logging
from .models import Post,Aboutus,Category
from django.http import Http404
from django.core.paginator import Paginator
from .forms import Forgotpasswordform, contactform,Registerform,Loginform,resetpasswordform,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group


# Create your views here.
#static data
#posts=[
#        
#             {'id':'1','title':'title 1','content':'content1'},
#           { 'id':'2','title':'title 2','content':'content2'},
#              {'id':'3','title':'title 3','content':'content3'},
#               {'id':'4','title':'title 4','content':'content4' },
#    ]
def index(request):
    blog_title = 'Sun news'
    #getting data from post models
    
    all_posts = Post.objects.filter(is_published=True) 
    paginator=Paginator(all_posts,6)
    page_number =request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    

    return render(request,'index.html',{'key': blog_title,'page_obj':page_obj})


def details(request,slug):
    #getting data by id in static data
    #post= next((item for item in posts if item['id']==post_id),None)
    #logger = logging.getLogger('TESTING')
    #logger.debug(f'post variable is {post}')

    #getting data using id in database
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,"You do not have permission to view this post.")
        return redirect('blog:index')
    else:
        try:
    
         post=Post.objects.get(slug=slug)
         related_post=Post.objects.filter(category=post.category).exclude(pk=post.id)
        except Post.DoesNotExist:
           raise Http404("post does not exist")
    


    
    return render(request,'details.html', {'post':post,'related_post':related_post})



def contact(request):
    if request.method == "POST":
        form = contactform(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            
            logger.debug(
                f"POST data is {form.cleaned_data['name']}, "f"{form.cleaned_data['email']}, "f"{form.cleaned_data['message']}")
            success_message = "your form has been submited!"
            return render(request, 'contact.html', {"form": form,'success_message':success_message})    
    

        else:
           

           logger.debug(
             f"form validation is failed"
           )
           return render(request, 'contact.html', {"form": form,'name':name,'email':email,'message':message})    
    return render(request, 'contact.html',)

def aboutus(request):
   aboutcontent = Aboutus.objects.first()
   if aboutcontent is None or not aboutcontent.content:
      aboutcontent ="it is a default content"
   else:
      aboutcontent=aboutcontent.content   
   return render(request,'about.html',{'content':aboutcontent})

def register(request):
    if request.method == "POST":
        form = Registerform(request.POST)
        print("form is received")
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            reader_group,created = Group.objects.get_or_create(name='readers')
            user.groups.add(reader_group)
            messages.success(request,'registration successfully!.you can log in now!')
            return redirect('/login')

            print("✅ register data successfully!")
        else:
            print("❌ form is invalid")
            messages.warning(request,'registration failed!,try again')
            print(form.errors)
              # <-- shows exact reason
    else:
        form = Registerform() 
        print("GET request: showing blank form")
      
    return render(request, 'register.html', {'form': form})

def login(request):
    form=Loginform()
    if request.method=='POST':
        form=Loginform(request.POST)
        if form.is_valid():
            print("login success!")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 
            user =    authenticate(username=username,password=password)
            if user is not None:
               auth_login(request,user)
               return redirect("/dashboard")


    


    return render(request,'login.html',{'form':form})

@login_required

def dashboard(request):
    post_title="my posts"
    
    all_posts=Post.objects.filter(user = request.user)
    paginator=Paginator(all_posts,6)
    page_number =request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context = {
        'post_title': post_title,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),  # <- important
    }
    
    return render(request,'dashboard.html',context)

def logout(request):
    auth_logout(request)
    return redirect('/')

def forgot_password(request):
    form=Forgotpasswordform()
    if request.method=="POST":
        form = Forgotpasswordform(request.POST)
        
        if form.is_valid():
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            user = User.objects.get(email = email, username=username)
            token=default_token_generator.make_token(user)
            uid= urlsafe_base64_encode(force_bytes(user.pk))
            current_site=get_current_site(request)
            subject="reset password requested"
            domain = current_site.domain
            message = render_to_string('blog/templates/reset_password_email.html',{'domain':domain,'uid':uid,'token':token})
            send_mail(subject,message,'noreply@example.com',[email])
            messages.success(request,'the email has been sent successfully!')

    return render(request,'forgot_password.html',{'form':form})

def Reset_password(request, uidb64 , token):
    form = resetpasswordform()
    if request.method =="POST":
        form = resetpasswordform(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user = None 
                
            if user is not None and default_token_generator.check_token(user,token):
                user.set_password(new_password) 
                user.save()
                messages.success(request,'your password has been reset successfully!')   
                return redirect('blog:login')
            else:
                messages.error(request,'the password has been reset successfully!')
                
    return render(request,'reset_password.html',{'form':form})

@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
    categories = Category.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')
    else:
        form = PostForm()

    return render(request, "new_post.html", {
        'categories': categories,
        'form': form
    })

@login_required
@permission_required('blog.change_post',raise_exception=True)
def edit_post(request,post_id):
    categories = Category.objects.all() 
    post = get_object_or_404(Post,pk=post_id)
    form = PostForm(instance=post)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'your post has been updated successfully!')  
            
            return redirect('blog:dashboard')
        
    
    return render(request,'edit_post.html',{'post':post,'categories': categories,'form':form,})

@login_required
@permission_required('blog.delete_post',raise_exception=True)
def delete_post(request, post_id):
    post = get_object_or_404(Post,pk = post_id)
    post.delete()
    messages.success(request,'your post has been deleted successfully!')
    return redirect('blog:dashboard')
 
@login_required    
@permission_required('blog.can_publish_post',raise_exception=True)
def publish_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.is_published = True
    post.save()
    messages.success(request, 'Your post has been published successfully!')
    return redirect('blog:dashboard')

    