# -*- coding: utf-8 -*-
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class GeopositionWidget(forms.MultiWidget):
	class Media:
		js = (
			'vendor/openlayers/ol.js',
			'geoposition/geoposition.js',
		)
		css = {
			'screen': (
				'vendor/openlayers/ol.css',
				'geoposition/geoposition.css',
			)
		}

	def __init__(self, attrs=None):
		widgets = (
			forms.TextInput(),
			forms.TextInput(),
		)
		super().__init__(widgets, attrs)

	def decompress(self, value):
		if isinstance(value, str):
			return value.rsplit(',')
		if value:
			return [value.latitude, value.longitude]
		return [None, None]

	def render(self, name, value, *args, **kwargs):
		rendered = super().render(name, value, *args, **kwargs)
		return render_to_string('geoposition/widgets/geoposition_container.html', {
			'widget': mark_safe(rendered),
			'name': name,
		})
