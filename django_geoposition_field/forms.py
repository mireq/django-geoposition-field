# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

from .widgets import GeopositionWidget


class GeopositionField(forms.MultiValueField):
	default_error_messages = {
		'invalid': _("Enter a valid geoposition.")
	}

	def __init__(self, *args, **kwargs):
		self.widget = GeopositionWidget()
		fields = (
			forms.DecimalField(label=_('latitude')),
			forms.DecimalField(label=_('longitude')),
		)
		super().__init__(fields, **kwargs)

	def widget_attrs(self, widget):
		classes = widget.attrs.get('class', '').split()
		classes.append('geoposition')
		return {'class': ' '.join(classes)}

	def compress(self, value_list):
		if value_list:
			return '{0},{1}'.format(*value_list)
		return ''
