# -*- coding: utf-8 -*-
from decimal import Decimal


class Geoposition(object):
	__slots__ = ['latitude', 'longitude']

	def __init__(self, latitude, longitude):
		self.latitude = Decimal(str(latitude))
		self.longitude = Decimal(str(longitude))

	def __str__(self):
		return f'{self.latitude},{self.longitude}'

	def __repr__(self):
		return f'{self.__class__.__name__}({self.latitude}, {self.longitude})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.latitude == other.latitude and self.longitude == other.longitude

	def __ne__(self, other):
		return not isinstance(other, self.__class__) or self.latitude != other.latitude or self.longitude != other.longitude
