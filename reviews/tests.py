from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Review, Ticket, UserFollows


class ReviewModelsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(username='auteur')
        self.reader = user_model.objects.create_user(username='lecteur')
        self.ticket = Ticket.objects.create(
            title='Le Petit Prince',
            description='Que pensez-vous de ce livre ?',
            user=self.author,
        )

    def test_ticket_is_linked_to_its_author(self):
        self.assertEqual(self.ticket.user, self.author)
        self.assertEqual(str(self.ticket), 'Le Petit Prince')

    def test_review_accepts_rating_between_zero_and_five(self):
        review = Review(
            ticket=self.ticket,
            rating=5,
            headline='Une belle lecture',
            user=self.reader,
        )

        review.full_clean()
        review.save()

        self.assertEqual(review.ticket, self.ticket)

    def test_review_rejects_rating_above_five(self):
        review = Review(
            ticket=self.ticket,
            rating=6,
            headline='Note invalide',
            user=self.reader,
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_user_cannot_follow_same_user_twice(self):
        UserFollows.objects.create(
            user=self.author,
            followed_user=self.reader,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            UserFollows.objects.create(
                user=self.author,
                followed_user=self.reader,
            )

    def test_ticket_deletion_also_deletes_its_reviews(self):
        Review.objects.create(
            ticket=self.ticket,
            rating=4,
            headline='Très intéressant',
            user=self.reader,
        )

        self.ticket.delete()

        self.assertFalse(Review.objects.exists())


class PublicationViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username='proprietaire')
        self.other_user = user_model.objects.create_user(username='autre')
        self.ticket = Ticket.objects.create(
            title='Billet initial',
            user=self.owner,
        )
        self.review = Review.objects.create(
            ticket=self.ticket,
            rating=3,
            headline='Critique initiale',
            user=self.owner,
        )

    def test_authenticated_user_can_create_ticket(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('ticket-create'),
            {'title': 'Nouveau billet', 'description': 'Une description'},
        )

        self.assertRedirects(response, reverse('home'))
        ticket = Ticket.objects.get(title='Nouveau billet')
        self.assertEqual(ticket.user, self.owner)

    def test_owner_can_edit_ticket(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('ticket-edit', args=[self.ticket.id]),
            {'title': 'Billet modifié', 'description': ''},
        )

        self.assertRedirects(response, reverse('home'))
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.title, 'Billet modifié')

    def test_ticket_edit_page_displays_current_image(self):
        self.ticket.image = 'couverture-test.png'
        self.ticket.save()
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse('ticket-edit', args=[self.ticket.id])
        )

        self.assertContains(response, 'Image actuelle')
        self.assertContains(response, '/media/couverture-test.png')

    def test_other_user_cannot_edit_ticket(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('ticket-edit', args=[self.ticket.id]),
            {'title': 'Modification interdite', 'description': ''},
        )

        self.assertEqual(response.status_code, 404)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.title, 'Billet initial')

    def test_ticket_is_only_deleted_with_post(self):
        self.client.force_login(self.owner)
        url = reverse('ticket-delete', args=[self.ticket.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ticket.objects.filter(id=self.ticket.id).exists())

        response = self.client.post(url)

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_other_user_cannot_delete_ticket(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('ticket-delete', args=[self.ticket.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_authenticated_user_can_create_review(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('review-create', args=[self.ticket.id]),
            {
                'headline': 'Nouvelle critique',
                'rating': 5,
                'body': 'Excellent livre.',
            },
        )

        self.assertRedirects(response, reverse('home'))
        review = Review.objects.get(headline='Nouvelle critique')
        self.assertEqual(review.user, self.other_user)
        self.assertEqual(review.ticket, self.ticket)

    def test_owner_can_edit_review(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('review-edit', args=[self.review.id]),
            {
                'headline': 'Critique modifiée',
                'rating': 4,
                'body': '',
            },
        )

        self.assertRedirects(response, reverse('home'))
        self.review.refresh_from_db()
        self.assertEqual(self.review.headline, 'Critique modifiée')

    def test_other_user_cannot_edit_review(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('review-edit', args=[self.review.id]),
            {
                'headline': 'Modification interdite',
                'rating': 1,
                'body': '',
            },
        )

        self.assertEqual(response.status_code, 404)
        self.review.refresh_from_db()
        self.assertEqual(self.review.headline, 'Critique initiale')

    def test_review_is_only_deleted_with_post(self):
        self.client.force_login(self.owner)
        url = reverse('review-delete', args=[self.review.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

        response = self.client.post(url)

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_other_user_cannot_delete_review(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('review-delete', args=[self.review.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())
