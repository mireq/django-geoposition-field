# -*- coding: utf-8 -*-
from decimal import Decimal as D

from django import forms
from django.core import serializers
from django.http import QueryDict
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


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['location']


class TestGeopositionForm(TestCase):
	def test_invalid(self):
		q = QueryDict('', mutable=True)
		q['location_0'] = 'xxx'
		q['location_1'] = 'yyy'
		form = AddressForm(q)
		self.assertFalse(form.is_valid())

	def test_valid(self):
		q = QueryDict('', mutable=True)
		q['location_0'] = '1.5'
		q['location_1'] = '2.5'
		form = AddressForm(q)
		self.assertTrue(form.is_valid())
		address = form.save(commit=False)
		self.assertEqual(D('1.5'), address.location.latitude)
		self.assertEqual(D('2.5'), address.location.longitude)

	def test_initial(self):
		address = Address(location=Geoposition('1.5', '2.5'))
		form = AddressForm(instance=address)
		form_str = str(form)
		self.assertIn('"1.5"', form_str)
		self.assertIn('"2.5"', form_str)
		self.assertEqual(D('1.5'), form.initial['location'].latitude)
		self.assertEqual(D('2.5'), form.initial['location'].longitude)

	def test_empty(self):
		q = QueryDict('')
		form = AddressForm(q)
		self.assertTrue(form.is_valid())
		address = form.save(commit=True)
		address.refresh_from_db()
		self.assertIsNone(address.location)

	def test_decompress(self):
		form = AddressForm(initial={'location': '1.5,2.5'})
		form_str = str(form)
		self.assertIn('"1.5"', form_str)
		self.assertIn('"2.5"', form_str)

		form = AddressForm(initial={'location': Geoposition('1.5', '2.5')})
		form_str = str(form)
		self.assertIn('"1.5"', form_str)
		self.assertIn('"2.5"', form_str)

		form = AddressForm(initial={'location': None})
		form_str = str(form)
		self.assertNotIn('value=', form_str)
