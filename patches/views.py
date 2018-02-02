from django.shortcuts import render

from .patches import build


def activity(request):
    return render(request, "activity.html", {"activity": build()})
