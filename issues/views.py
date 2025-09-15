from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now, timedelta
from .forms import IssueForm
from .models import Issue, Vote, Like, Comment

@login_required
def like_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, issue=issue)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'like_count': issue.likes.count(),
        'liked': liked
    })

@login_required
def create_issue(request):
    if not request.user.is_verified:
        messages.warning(request, "Your profile is not verified yet. Please submit your NID and wait for approval.")
        return redirect('issue_list')

    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.anonymous = 'anonymous' in request.POST
            issue.save()
            return redirect('issue_list')
    else:
        form = IssueForm()
    return render(request, 'issues/create_issue.html', {'form': form})

def issue_list(request):
    """✅ Public feed: everyone can view issues"""
    issues = Issue.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')

    # For anonymous users, voted_ids & liked_ids will be empty
    if request.user.is_authenticated:
        voted_ids = Vote.objects.filter(user=request.user).values_list('issue_id', flat=True)
        liked_ids = Like.objects.filter(user=request.user).values_list('issue_id', flat=True)
    else:
        voted_ids = []
        liked_ids = []

    # ✅ Filtering
    division = request.GET.get('division')
    district = request.GET.get('district')
    upazila = request.GET.get('upazila')
    filters = {}
    if division: filters['division'] = division
    if district: filters['district'] = district
    if upazila: filters['upazila'] = upazila
    issues = issues.filter(**filters)

    return render(request, 'issues/issue_list.html', {
        'issues': issues,
        'voted_ids': voted_ids,
        'liked_ids': liked_ids,
        'current_filters': {
            'division': division or '',
            'district': district or '',
            'upazila': upazila or '',
        }
    })

@login_required
def my_posts(request):
    posts = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'issues/my_posts.html', {'posts': posts})

@login_required
def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if not request.user.is_govt:
        return redirect('issue_list')

    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, "Issue updated.")
            return redirect('issue_list')
    else:
        form = IssueForm(instance=issue)

    return render(request, 'issues/edit_issue.html', {'form': form})

@login_required
def delete_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.user.is_govt:
        issue.delete()
        messages.success(request, "Issue deleted.")
    return redirect('issue_list')

@login_required
def add_comment(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(issue=issue, user=request.user, content=content)
    return redirect('issue_list')

@login_required
def update_status(request, issue_id):
    if not request.user.is_govt:
        return redirect('issue_list')
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            issue.status = status
            issue.save()
            messages.success(request, "✅ Issue status updated!")
    return redirect('issue_list')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_govt:
        comment.delete()
        messages.success(request, "🗑️ Comment deleted.")
    return redirect('issue_list')
@login_required
def vote_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    already_voted = Vote.objects.filter(issue=issue, user=request.user).exists()
    if not already_voted:
        Vote.objects.create(issue=issue, user=request.user)
    return redirect('issue_list')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    posts = Issue.objects.filter(user=profile_user).order_by('-created_at')


    show_nid = (request.user == profile_user)

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'show_nid': show_nid
    })