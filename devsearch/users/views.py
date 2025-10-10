from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles


# Create your views here.
def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print('Username does not exist')
            messages.error(request, 'Username does not exist!')
            
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # return redirect('profiles')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            print('Username OR Password is incorrect!')
            messages.error(request, 'Username OR Password is incorrect!')

    return render(request, 'users/login_register.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Logout successfully!')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("IS POST")
        if form.is_valid():
            print("IS VALID")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error was occurred during registration!')

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = search_profiles(request)

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1
    
    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    context ={
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="") 
    other_skills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all() 
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def add_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST,)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(request, 'Skill was added successfully!')

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {
        'object': skill
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_request = profile.messages.all()
    unread_count = message_request.filter(is_read=False).count()
    context = {
        "message_request": message_request,
        "unread_count": unread_count
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {
        'message': message
    }
    return render(request, 'users/message.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('user_profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)