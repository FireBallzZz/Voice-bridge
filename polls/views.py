from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PollForm
from .models import Poll, Vote

@login_required
def create_poll(request):
    if not request.user.is_govt:
        return redirect('home')  # only govt can access

    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')

        if question and option1 and option2:
            Poll.objects.create(
                question=question,
                option1=option1,
                option2=option2,
                option3=option3 or None,
                option4=option4 or None,
                created_by=request.user
            )
            return redirect('poll_list')
        else:
            return render(request, 'polls/create_poll.html', {'error': 'Question and at least 2 options are required.'})

    return render(request, 'polls/create_poll.html')
@login_required
def poll_list(request):
    polls = Poll.objects.all()

    for poll in polls:
        poll.total_votes = Vote.objects.filter(poll=poll).count()
        poll.option1_votes = Vote.objects.filter(poll=poll, choice=poll.option1).count()
        poll.option2_votes = Vote.objects.filter(poll=poll, choice=poll.option2).count()
        poll.option3_votes = Vote.objects.filter(poll=poll, choice=poll.option3).count() if poll.option3 else 0
        poll.option4_votes = Vote.objects.filter(poll=poll, choice=poll.option4).count() if poll.option4 else 0

    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    choice = request.POST.get('choice')
    if choice:
        Vote.objects.update_or_create(
            user=request.user,
            poll=poll,
            defaults={'choice': choice}
        )
        messages.success(request, "✅ Your vote has been submitted!")
    else:
        messages.error(request, "⚠️ Please select an option before submitting.")

    return redirect('poll_list')
@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Poll updated successfully.")
            return redirect('poll_list')
    else:
        form = PollForm(instance=poll)
    return render(request, 'polls/create_poll.html', {'form': form})


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    poll.delete()
    messages.success(request, "🗑️ Poll deleted.")
    return redirect('poll_list')
