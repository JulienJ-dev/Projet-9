from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm, TicketForm
from .models import Review, Ticket


@login_required
def ticket_create(request):
    form = TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect('home')

    return render(
        request,
        'reviews/ticket_form.html',
        {'form': form, 'page_title': 'Créer un billet'},
    )


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user,
    )
    form = TicketForm(
        request.POST or None,
        request.FILES or None,
        instance=ticket,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    return render(
        request,
        'reviews/ticket_form.html',
        {
            'form': form,
            'ticket': ticket,
            'page_title': 'Modifier votre billet',
        },
    )


@login_required
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user,
    )
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    return render(
        request,
        'reviews/ticket_confirm_delete.html',
        {'ticket': ticket},
    )


@login_required
def review_create(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.ticket = ticket
        review.user = request.user
        review.save()
        return redirect('home')

    return render(
        request,
        'reviews/review_form.html',
        {
            'form': form,
            'ticket': ticket,
            'page_title': 'Créer une critique',
        },
    )


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )
    form = ReviewForm(request.POST or None, instance=review)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    return render(
        request,
        'reviews/review_form.html',
        {
            'form': form,
            'ticket': review.ticket,
            'page_title': 'Modifier votre critique',
        },
    )


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )
    if request.method == 'POST':
        review.delete()
        return redirect('home')

    return render(
        request,
        'reviews/review_confirm_delete.html',
        {'review': review},
    )
