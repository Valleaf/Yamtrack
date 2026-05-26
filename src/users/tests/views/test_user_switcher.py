from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserSwitcherTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.all().delete()
        self.val = User.objects.create_user(username="Val", password="val123")
        self.imane = User.objects.create_user(username="Imane", password="imane123")

    def test_sidebar_shows_user_toggle_without_logout(self):
        self.client.login(username="Val", password="val123")

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Val")
        self.assertContains(response, "Imane")
        self.assertContains(response, reverse("switch_user"))
        self.assertNotContains(response, "Logout")
        self.assertNotContains(response, reverse("account_logout"))

    def test_switch_user_toggles_between_default_users(self):
        self.client.login(username="Val", password="val123")

        response = self.client.post(reverse("switch_user"))

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.imane.id)
