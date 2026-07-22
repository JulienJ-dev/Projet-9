from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")

    return render(
        request,
        "authentication/signup.html",
        {"form": form},
    )


@login_required
def home(request):
    tickets = request.user.ticket_set.order_by('-time_created')
    reviews = request.user.review_set.select_related('ticket').order_by(
        '-time_created'
    )
    return render(
        request,
        'authentication/home.html',
        {'tickets': tickets, 'reviews': reviews},
    )
