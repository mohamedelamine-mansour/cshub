from django.shortcuts import render

from .models import Community


def home(request):
    communities = Community.objects.all()
    return render(request, 'forum/home.html', {'communities': communities})