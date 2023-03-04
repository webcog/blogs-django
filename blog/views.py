from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Post, Profile
from .forms import NewUserForm, User_Post, User_Profile
from django.contrib.auth import login
from django.contrib import messages
from django.utils.text import slugify
import math
from django.http import HttpResponse


# Create your views here.
@login_required
def category(request):
    categories = Category.objects.all()


    no_of_posts = 6
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    print(page)
    categories = Category.objects.all()
    length = len(categories)
    categories =categories[(page-1)*no_of_posts: page*no_of_posts]
    if page>1:
        prev = page - 1
    else:
        prev = None
    
    if page<math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None    

    context = {
        'categories': categories,
        'prev':prev,
        'nxt':nxt,
    }
    return render(request, 'home.html', context)

@login_required
def post(request):
    no_of_posts = 4 
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    posts = Post.objects.all().order_by('-id')
    length = len(posts)
    posts =posts[(page-1)*no_of_posts: page*no_of_posts]
    if page>1:
        prev = page - 1
    else:
        prev = None
    
    if page<math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None    
    data={
        'posts':posts,
        'prev':prev,
        'nxt':nxt,
    }
    return render(request, 'posts.html',data)
@login_required
def view_posts(request, slug):
    posts = Post.objects.filter(slug=slug)
    context = {
        'posts':posts,
    }
    return render(request, 'view_post.html', context)

@login_required
def post_details(request, slug):
    post = Post.objects.get(slug=slug)
    context = {'post': post,}
    return render(request, 'post_details.html', context)


@login_required
def cat_post(request, id):
    category = Category.objects.get(id=id)
    posts = Post.objects.filter(category=category)
    context = {
        'category':category,
        'posts':posts,
    }
    return render(request, 'cat_post.html', context)



def signup(request):
        form = NewUserForm()
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Account Created Successfully")
                return redirect("login")
        return render (request, "signup.html", {"form":form})


@login_required
def setting(request, id):
    profile =  Profile.objects.get(id=id)
    form = User_Profile(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
            if request.user == profile.user:
                form.save()
                return redirect('user', profile.id)
            else:
                return HttpResponse("Access Denied")
    context = {
        'form':form,
        'profile':profile,
    }
    return render(request, 'account-setting.html', context)


@login_required
def user(request, id):
    current_user = request.user
    profile = Profile.objects.get(id = current_user.id)
    posts = Post.objects.filter(created_by=current_user.id).order_by('-id')
    context = {
        'current_user':current_user,
        'posts':posts,
        'profile':profile,
    }
    return render(request,'user.html', context)


@login_required
def upload_post(request):
    if request.method == 'POST':
        form = User_Post(request.POST or None, request.FILES or None)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.created_by = request.user
            if not blogpost.slug:
                blogpost.slug = slugify('{}{}-{}{}{}'.format(blogpost.title, blogpost.created_by,blogpost.category,blogpost.id,blogpost.created_at))
            blogpost.save()
            return redirect('post')
    form = User_Post()
    context = {
        'form':form,
        
    }
    return render(request,'upload_post.html', context)


def cat_post_delete(request, slug):
    posts = Post.objects.get(slug=slug)
    posts.delete()
    return redirect(post)

def post_delete(request, slug):
    posts = Post.objects.get(slug=slug)
    posts.delete()
    return redirect(post)

def user_post_delete(request,id, slug):
    posts = Post.objects.get(slug=slug)
    posts.delete()
    return redirect(post)

def test(request):
    x = input(">> ")
    return HttpResponse(x)
    return render(request,'test.html')





