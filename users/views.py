from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, EditProfileForm
from issues.models import Issue
from .models import CustomUser
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(CustomUser, username=username)
    posts = Issue.objects.filter(user=user_obj).order_by('-created_at')

    is_own_profile = request.user == user_obj

    return render(request, 'users/profile.html', {
        'profile_user': user_obj,
        'posts': posts,
        'is_own_profile': is_own_profile
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_govt:
        unverified_users = CustomUser.objects.filter(is_govt=False, is_verified=False).exclude(nid_number__isnull=True)


        last_30_days = timezone.now() - timedelta(days=30)
        from django.db.models import Count
        issue_summary = Issue.objects.filter(created_at__gte=last_30_days).values(
            'division', 'district', 'upazila'
        ).annotate(total=Count('id')).order_by('-total')

        return render(request, 'users/govt_dashboard.html', {
            'unverified_users': unverified_users,
            'issue_summary': issue_summary
        })
    else:
        pending_users = CustomUser.objects.filter(is_govt=False, is_verified=False).exclude(nid_number__isnull=True)
        return render(request, 'users/dashboard.html', {'pending_users': pending_users})



@login_required
def submit_nid(request):
    if request.method == 'POST':
        nid = request.POST.get('nid_number')
        if nid:
            request.user.nid_number = nid
            request.user.save()
            messages.success(request, "✅ NID submitted successfully. Please wait for government approval.")
        else:
            messages.error(request, "❌ Please enter a valid NID.")
    return redirect('profile', username=request.user.username)


@login_required
def approve_user(request, user_id):
    if not request.user.is_govt:
        return redirect('dashboard')

    user_to_verify = get_object_or_404(CustomUser, id=user_id)
    user_to_verify.is_verified = True
    user_to_verify.save()
    messages.success(request, f"✅ {user_to_verify.username} is now verified.")
    return redirect('dashboard')
