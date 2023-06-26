from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Conference, Session


def all_conferences(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/all_conferences.html', {'conferences': conferences})


def view_single_conference(request, id):
    conference = get_object_or_404(Conference, id=id)
    sessions = Session.objects.filter(conference=conference)
    return render(request, 'conference/single_conference.html', {
        'conference': conference,
        'sessions': sessions
    })


def create_conference(request):
    if request.method == 'POST':
        title = request.POST['title']
        date = request.POST['date']
        conference = Conference.objects.create(title=title, date=date)
        return redirect('conferences:view_single_conference', id=conference.id)
    return render(request, 'conference/create_conference.html')


def update_conference(request, id):
    conference = get_object_or_404(Conference, id=id)

    if request.method == 'POST':
        # Retrieve form data
        title = request.POST['title']
        date = request.POST['date']
        location = request.POST['location']

        conference.title = title
        conference.date = date
        conference.location = location
        conference.save()

        return redirect('view_single_conference', id=conference.id)

    context = {
        'conference': conference
    }
    return render(request, 'conference/update_conference.html', context)


def delete_conference(request, id):
    conference = get_object_or_404(Conference, id=id)

    if request.method == 'POST':
        # Delete conference object
        conference.delete()

        # Redirect to all conferences page
        return redirect('all_conferences')

    context = {
        'conference': conference
    }
    return render(request, 'conference/delete_conference.html', context)
