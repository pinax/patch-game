import random

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from account.decorators import login_required

from .factories import apps, generate_items
from .models import Showing, Response, UserState


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
    user_state = UserState.state_for_user(request.user)
    items = generate_items(user_state.data)
    if len(items) > 0:
        item = items[random.choice(list(items))]
        showing = Showing.objects.create(user=request.user, data=item)
        user_state.store("last_asked", item["answer"])
    else:
        showing = None
    return render(request, "activity.html", {
        "showing": showing,
        "correct_answers": list(user_state.data.get("last_correct", {}))
    })


@require_POST
@login_required
def response(request, pk):
    showing = get_object_or_404(Showing, user=request.user, pk=pk)
    Response.objects.create(showing=showing, answer={"answer": request.POST.get("answer")})
    return redirect("activity")
