from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView

from account.decorators import login_required

from .factories import apps, generate_items
from .models import ActivityItem, ActivitySession, SessionItem, ItemShowing, Response


class HomePage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "apps": apps
        })
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("activity")
        return super().get(request, *args, **kwargs)


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
    return render(request, "activity.html", {
        "activity": item.data,
        "item_showing": item_showing,
        "correct_answers": Response.objects.filter(
            score=100,
            item__item__session__user=request.user
        ).distinct()
    })


@login_required
def response(request, pk):
    item_showing = get_object_or_404(ItemShowing, item__session__user=request.user, pk=pk)
    Response.objects.create(item=item_showing, answer={"answer": request.POST.get("answer")})
    return redirect("activity")
