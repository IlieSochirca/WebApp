from django.test import TestCase
from django.urls import reverse
from ..models import Group

class LoginRequiredNewGroupTests(TestCase):
    def setUp(self):
        Group.objects.create(name='Autos', category='Sport', description='AutoLovers')