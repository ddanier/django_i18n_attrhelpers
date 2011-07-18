# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

def south_field_triple(self):
	from south.modelsinspector import introspector
	field_class = self.__class__.__module__ + "." + self.__class__.__name__
	args, kwargs = introspector(self)
	return (field_class, args, kwargs)

TRANSLATED_LANGUAGES = [(code, _(name)) for code, name in settings.LANGUAGES]


class LanguageField(models.CharField):
	def __init__(self, *args, **kwargs):
		kwargs['verbose_name'] = kwargs.get('verbose_name', _(u'Language'))
		kwargs['max_length'] = kwargs.get('max_length', 5)
		kwargs['choices'] = kwargs.get('choices', TRANSLATED_LANGUAGES)
		super(LanguageField, self).__init__(*args, **kwargs)
	
	south_field_triple = south_field_triple
