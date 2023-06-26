from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(user=user, request=request)
            return HttpResponseRedirect(redirect_to='/conferences')
        else:
            return HttpResponseRedirect(redirect_to='/login')

    return render(request, 'eventPlanner/login.html')


def home_view(request):
    conferences = Conference.objects.all()
    return render(request, 'conference/all_conferences.html', {'conferences': conferences})


def about_view(request):
    return HttpResponse("<h1>About Page</h1><br/><a href='/'>Go back to home</a>")


def testing_stuff(request, number):
    # DB query
    #
    # number = ''
    # if id < 5:
    #     number = 'xzy'
    return render(request, 'testing.html', {'number': number})
