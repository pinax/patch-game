# from django.core.urls import redirect
from django.shortcuts import redirect, render, get_object_or_404

from account.decorators import login_required

from .factories import generate_items
from .models import ActivityItem, ActivitySession, SessionItem, ItemShowing, Response


@login_required
def activity(request):
    session, created = ActivitySession.objects.get_or_create(user=request.user)
    if created:
        items = generate_items()
        for app in items.keys():
            ActivityItem.objects.create(data=items[app])
    item = ActivityItem.objects.all().order_by("?").first()
    session_item, _ = SessionItem.objects.get_or_create(item=item, session=session)
    item_showing = ItemShowing.objects.create(item=session_item)
    return render(request, "activity.html", {"activity": item.data, "item_showing": item_showing})


@login_required
def response(request, pk):
    item_showing = get_object_or_404(ItemShowing, item__session__user=request.user, pk=pk)
    Response.objects.create(item=item_showing, answer={"answer": request.POST.get("answer")})
    return redirect("activity")
