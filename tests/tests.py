# -*- coding: utf-8 -*-
from django.test import TestCase

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
