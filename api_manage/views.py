from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from .models import BlogPost  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required





@login_required
def home_page(request ):

    
        blogs = BlogPost.objects.filter(visibility='public' , status = 'published')

        
        
        private = BlogPost.objects.filter(
                    visibility='private',
                    status='published',
                    author=request.user
                )
        
        #for seraching
        title_query = request.GET.get('title')

        if title_query:
            blogs = blogs.filter(title__icontains=title_query)

        pk = request.user.id # get the session id 
        
        private_blogs = BlogPost.objects.filter(user = pk , visibility='private' )


        username = request.user.username
        #geting username coz we used login functiom so that we get the session username


        return render(request , 'home_page.html' , {'blogs': blogs , 'private':private , "title_query": title_query , "private_blogs":private_blogs ,  "username":username } )

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/user_auth/')


def user_auth(request):

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")

            return redirect('/user_auth/')
        
        login(request, user)

        return redirect('/home/')

    
    return render(request, 'user_auth.html')



def register(request):

    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

            return redirect('/register/')
        
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")

        return redirect('/user_auth/')
    return render(request, 'register.html')

@login_required
def create_blog(request):
    
    user = request.user.id 

    
    user_id = get_object_or_404(User , pk = user)

    
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        created_date = request.POST.get("created_date")
        status = request.POST.get("status")
        visibility = request.POST.get("visibility")
        update_date = created_date

        

        BlogPost.objects.create(
            user = user_id,
            title=title,
            content=content,
            author=user_id.username,
            created_date=created_date,
            update_date=update_date,
            status=status,
            visibility = visibility
        )

        messages.success(request, "Blog created successfully.")
        return redirect(f'/home/')

    return render(request, 'create.html')


@login_required
def manage(request):
    
    username = request.user.username

    user = get_object_or_404(User, username=username)

    
    blogs = BlogPost.objects.filter(user=user)

    
    title_query = request.GET.get('title')
    if title_query:
        blogs = blogs.filter(title__icontains=title_query)

    
    selected_status = request.GET.get('status')
    if selected_status:
        blogs = blogs.filter(status=selected_status)

    context = {
        "user": user,
        "blogs": blogs,
        "selected_status": selected_status,
        "title_query": title_query,
    }

    return render(request, 'manage.html', context)


@login_required
def update_blog(request):

    
    user_id = request.GET.get('blog_id')
    
   
    blog = get_object_or_404(BlogPost, pk=user_id)

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.status = request.POST.get('status')
        blog.visibility = request.POST.get("visibility")
        blog.update_date = date.today()
        blog.save()

        messages.success(request, "Blog updated successfully.")
        
        return  redirect(f'/manage/')

    return render(request, 'update_blog.html', {"blog": blog})

@login_required
def delete_blog(request):
    user_id = request.GET.get('blog_id' )

    
    blog = get_object_or_404(BlogPost, pk=user_id)



    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect(f'/manage/')

    return render(request, 'delete_blog.html', {'blog': blog})


