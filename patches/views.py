from django.shortcuts import render

from .factories import build


def activity(request):
    return render(request, "activity.html", {"activity": build()})
