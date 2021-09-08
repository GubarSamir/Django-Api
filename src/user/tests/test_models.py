from django.test import TestCase
from django.contrib.auth import get_user_model

from user.models import Author


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'user_1@test.com'
        password = 'test_passwd'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        email = 'user_1@TEST.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='password123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='password123'
            )



class AuthorModelTest(TestCase):


    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')


    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')


    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')


    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)


    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))


    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')