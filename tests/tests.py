# -*- coding: utf-8 -*-
from django.core import serializers
from django.test import TestCase

from .models import Address
from django_geoposition_field import Geoposition


class TestGeopositionObject(TestCase):
	def test_geoposition(self):
		position = Geoposition(1, 2)
		equals_position = Geoposition(1, 2)
		other_position = Geoposition(1, 3)
		self.assertEqual('1,2', str(position))
		self.assertEqual('Geoposition(1, 2)', repr(position))
		self.assertEqual(position, equals_position)
		self.assertNotEqual(position, other_position)


class TestGeopositionModel(TestCase):
	def test_empty_address(self):
		addr = Address.objects.create()
		addr.refresh_from_db()
		self.assertIsNone(addr.location)

	def test_saved_value(self):
		addr = Address.objects.create(location=Geoposition(1, 2))
		addr.refresh_from_db()
		self.assertEqual(1, addr.location.latitude)
		self.assertEqual(2, addr.location.longitude)

	def test_invalid_value(self):
		addr = Address.objects.create()
		Address.objects.update(location='invalid')
		addr.refresh_from_db()
		self.assertIsNone(addr.location)

	def test_serialization(self):
		Address.objects.create(location=Geoposition('1.5', '2.5'))
		data = serializers.serialize('json', Address.objects.all())
		address = list(serializers.deserialize('json', data))[0].object
		self.assertEqual(Geoposition('1.5', '2.5'), address.location)
		self.assertEqual(None, address.location2)
