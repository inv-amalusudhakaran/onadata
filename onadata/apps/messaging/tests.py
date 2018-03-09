# -*- coding: utf-8 -*-
"""
Tests Messaging app implementation.
"""
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from actstream.models import Action

from onadata.apps.messaging.viewsets import MessagingViewSet


def _create_user(username='testuser'):
    return User.objects.create(username=username)


class TestMessagingViewSet(TestCase):
    """
    Test MessagingViewSet class.
    """

    def setUp(self):
        self.factory = APIRequestFactory()

    def _create_message(self):
        """
        Helper to create a single message
        """
        user = _create_user()
        view = MessagingViewSet.as_view({'post': 'create'})
        data = {
            "message": "Hello World!",
            "target_id": user.pk,
            "target_type": 'user',
        }  # yapf: disable
        request = self.factory.post('/messaging', data)
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(data, response.data)

        return response.data

    def test_create_message(self):
        """
        Test POST /messaging adding a new message for a specific form.
        """
        self._create_message()

    def test_target_does_not_exist(self):
        """
        Test POST /messaging adding a new message for a specific form with a
        target that does not exist.
        """
        user = _create_user()
        view = MessagingViewSet.as_view({'post': 'create'})
        data = {
            "message": "Hello World!",
            "target_id": 1000000000,
            "target_type": 'user',
        }  # yapf: disable
        request = self.factory.post('/messaging', data)
        force_authenticate(request, user=user)
        response = view(request=request)
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(response.data['target_id'], 'target_id not found')

    def test_delete_message(self):
        """
        Test DELETE /messaging/[pk] deleting a message.
        """
        message_data = self._create_message()
        view = MessagingViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete('/messaging/%s' % message_data['id'])
        response = view(request=request, pk=message_data['id'])
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Action.objects.filter(pk=message_data['id']).exists())

    def test_list_messages(self):
        """
        Test GET /messaging listing of messages for specific forms.
        """
        message_data = self._create_message()
        view = MessagingViewSet.as_view({'get': 'list'})
        request = self.factory.get('/messaging')
        response = view(request=request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [message_data])

    def test_retrieve_message(self):
        """
        Test GET /messaging/[pk] return a message matching pk.
        """
        message_data = self._create_message()
        view = MessagingViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/messaging/{}'.format(message_data['id']))
        response = view(request=request, pk=message_data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, message_data)

    def test_authentication_required(self):
        """
        Test that authentication is required at all endpoints.
        """
        self.fail('Implement authentication required.')
