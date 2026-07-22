from django.urls import path

from . import views


urlpatterns = [
    path('billets/ajouter/', views.ticket_create, name='ticket-create'),
    path(
        'billets/<int:ticket_id>/modifier/',
        views.ticket_edit,
        name='ticket-edit',
    ),
    path(
        'billets/<int:ticket_id>/supprimer/',
        views.ticket_delete,
        name='ticket-delete',
    ),
    path(
        'billets/<int:ticket_id>/critiquer/',
        views.review_create,
        name='review-create',
    ),
    path(
        'critiques/<int:review_id>/modifier/',
        views.review_edit,
        name='review-edit',
    ),
    path(
        'critiques/<int:review_id>/supprimer/',
        views.review_delete,
        name='review-delete',
    ),
]
