from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest


# Login form backend
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                subject = "Welcome back, " + user.username
                message = "You have successfully logged in to your account."
                send_mail(subject, message, 'universalcollege718@gmail.com', [user.email])
                return redirect('feed')
    else:
        form = LoginForm()        
    return render(request, 'baseapp/login.html', {'form': form})


# Signup from backend
def signup(request):
   
    if request.method == 'POST':
        
        username = request.POST['username'] 
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        def is_valid_password(password1):
    # Check the length of the password (minimum 8 characters).
            if len(password1) < 8:
                return False

    # Check for at least one uppercase letter.
            if not any(char.isupper() for char in password1):
                return False

    # Check for at least one lowercase letter.
            if not any(char.islower() for char in password1):
                return False

    # Check for at least one digit.
            if not any(char.isdigit() for char in password1):
                return False

    # Check for at least one special character (e.g., !@#$%^&*()).
            if not re.search(r'[!@#$%^&*()]', password1):
                return False

    # All conditions passed; the password is valid.
            return True

    
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, f"The user already exist")
            elif User.objects.filter(email = email).exists():
                messages.error(request, f"The email already exist")
            elif is_valid_password(password1) == False:
                messages.error(request, f"The password is not so strong.")
            else:
                data = User.objects.create_user(username = username, email = email, password = password1)  
                data.save()
                subject = "Welcome to the ConnectHub, " + username
                message = "You have successfully signed up for an account."
                send_mail(subject, message, 'universalcollege718@gmail.com', [email])
                return redirect('login')    
        else:
            messages.error(request, f"The passwords doesnt match.")
            return redirect('signup')

    return render(request, 'baseapp/signup.html') 



# def home(request):


#     return render(request, 'baseapp/home.html')
@login_required(login_url='login')
def feed(request):
    profile = UserProfile.objects.get(user = request.user)
    
    all_posts = Post.objects.all().order_by('-created_at')  # Order by latest first
    context = {
        'all_posts': all_posts,
        'profile' : profile
               }
    
    return render(request, 'baseapp/feed.html', context)

@login_required(login_url='login')
def like(request):

    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter  = LikePost.objects.filter(post_id = post_id, username = username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('feed')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('feed')





@login_required(login_url='login')
def editprofile(request):


    profile = UserProfile.objects.get(user=request.user)
    if request.method =='POST':
        profile.name = request.POST.get('name')
        profile.phoneno = request.POST.get('phoneno')
        profile.bio = request.POST.get('bio')
        profile.dob = request.POST.get('dob')
        profile.gender = request.POST.get('gender')
        if 'coverImg' in request.FILES:
            profile.coverImg = request.FILES.get('coverImg')
        if 'profileImg' in request.FILES:
            profile.profileImg = request.FILES.get('profileImg')
        profile.save()

        return redirect('profileview')




    return render(request, 'baseapp/editprofile.html',{'profile' : profile})

@login_required(login_url='login')
def profileview(request):
    profile = UserProfile.objects.get(user=request.user)

    all_posts = Post.objects.filter(user = request.user).order_by('-created_at')

    context = {
        'all_posts':all_posts,
        'profile':profile
        }
    return render(request,  'baseapp/profileview.html',context)

@login_required(login_url='login')
def profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username) 
    

    context = {
       
        'profile': profile,
       
    }
    return render(request,  'baseapp/profile.html', context)


@login_required
def follow_user(request, user_id):
  user_to_follow = User.objects.get(pk=user_id)
  if user_to_follow != request.user:
    Follow.objects.create(follower=request.user, following_user=user_to_follow)
  return redirect('/profile/' + user_id)

@login_required
def unfollow_user(request, user_id):
  user_to_unfollow = User.objects.get(pk=user_id)
  follow_obj = Follow.objects.filter(follower=request.user, following_user=user_to_unfollow).first()
  if follow_obj:
    follow_obj.delete()
  return redirect('/profile/' + user_id)






@login_required(login_url='login')
def post(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        upload = request.FILES.get('upload')
        title = request.POST.get('title')
        caption = request.POST.get('caption')

        new_post = Post.objects.create(user = request.user , caption = caption, title = title , upload = upload )
        new_post.save()
        return redirect('feed')
    
    context = {
        'profile':profile
        }

    return render(request, 'baseapp/post.html', context)


# def post_detail(request, pk):
#     post = Post.objects.get(pk=pk)
#     comments = post.comments.order_by('-created_date')  # Order comments by creation date (descending)
#     if request.method == 'POST':
#         if request.POST.get('comment_text'):  # Check if comment text exists in POST data
#             comment_text = request.POST['comment_text']
#             author = request.POST.get('author', '')  # Get author name (optional)
#             if comment_text:  # Check if comment text is not empty
#                 comment = Comment.objects.create(comment_text=comment_text, post=post, author=author)
#                 return redirect('post_detail', pk=pk)  # Redirect to same post detail page
#             else:
#                 return HttpResponseBadRequest('Please enter a comment.')  # Handle empty comments
#         else:
#             return HttpResponseBadRequest('Invalid request.')  # Handle missing data
#     context = {'post': post, 'comments': comments}
#     return render(request, 'baseapp/post_detail.html', context)



@login_required(login_url='login')
def message(request):
    
    return render(request,"baseapp/message.html")

@login_required(login_url='login')
def notification(request):
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile':profile
        }
    return render(request, 'baseapp/notification.html',context)

@login_required(login_url='login')
def search(request):
    profile = UserProfile.objects.get(user=request.user)
    query = request.GET.get('query')
    users = []

    if query:
        users = UserProfile.objects.filter(name__icontains=query)

    context = {
        'profile':profile,
        'users': users,
        'query': query
        }
    return render(request, 'baseapp/search.html',context)

@login_required(login_url='login')
def discover(request):

    profile = UserProfile.objects.get(user=request.user)

    all_posts = Post.objects.all().order_by('-created_at')  # Order by latest first
    context = {
        'all_posts': all_posts,
        'profile' : profile
               }

    return render(request, 'baseapp/discover.html',context)

@login_required(login_url='login')
def settings(request):

    profile = UserProfile.objects.get(user=request.user)

    context = {
        'profile':profile
        }

    return render(request, 'baseapp/settings.html',context)
@login_required(login_url='login')    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')