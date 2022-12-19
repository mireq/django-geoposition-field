# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.paginator import InvalidPage
from django.db.models import F
from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Address


class TestGeopositionField(TestCase):
	def test_to_pyton(self):
		print("ok")
