from django.utils.translation import get_language
try:
    # >= Django 1.5
    from django.db.models.constants import LOOKUP_SEP
except ImportError:
    # < Django 1.5
    from django.db.models.sql.constants import LOOKUP_SEP
from django.db import models

from django_i18n_attrhelpers.models import I18NAttribute


def localized_query_set_factory(BaseQuerySet=models.query.QuerySet):
	class LocalizedQuerySet(BaseQuerySet):
		def __init__(self, model=None, query=None, language_attr='language', *args, **kwargs):
			super(LocalizedQuerySet, self).__init__(model, query, *args, **kwargs)
			self.language_attr = language_attr
			self.language = None
		
		def _clone(self, klass=None, setup=False, **kwargs):
			c = super(LocalizedQuerySet, self)._clone(klass, setup, **kwargs)
			c.language_attr = self.language_attr
			c.language = self.language
			return c
		
		def localize(self, language_code=None):
			from django.core.exceptions import FieldError
			if language_code is None:
				language_code = get_language()
			clone = self._clone()
			clone.language = language_code
			if self.language_attr:
				try:
					clone = clone.filter(**{self.language_attr: language_code})
				except (AttributeError, FieldError):
					pass
			return clone
		
		def _filter_or_exclude(self, negate, *args, **kwargs):
			localized_kwargs = {}
			if self.language:
				for lookup in kwargs:
					parts = lookup.split(LOOKUP_SEP)
					fieldname = parts[0]
					localized_fieldname = fieldname
					if fieldname in getattr(self.model, '_i18n_attributes', ()):
						localized_fieldname = '%s_%s' % (fieldname, self.language)
					localized_lookup = LOOKUP_SEP.join([localized_fieldname] + parts[1:])
					localized_kwargs[localized_lookup] = kwargs[lookup]
			else:
				localized_kwargs = kwargs
			return super(LocalizedQuerySet, self)._filter_or_exclude(negate, *args, **localized_kwargs)
		
		def order_by(self, *field_names):
			if self.language:
				localized_field_names = []
				for field_name in field_names:
					localized_fieldname = field_name
					if field_name in getattr(self.model, '_i18n_attributes', ()):
						localized_fieldname = '%s_%s' % (field_name, self.language)
					localized_field_names.append(localized_fieldname)
			else:
				localized_field_names = field_names
			return super(LocalizedQuerySet, self).order_by(*localized_field_names)
	
	return LocalizedQuerySet


def localized_manager_factory(BaseManager=models.Manager, LocalizedQuerySet=None):
	if LocalizedQuerySet is None:
		LocalizedQuerySet = localized_query_set_factory()
	
	class LocalizedManager(BaseManager):
		def __init__(self, language_attr='language', *args, **kwargs):
			self.language_attr = language_attr
			super(LocalizedManager, self).__init__(*args, **kwargs)
		
		def _construct_query_set(self, cls, *args, **kwargs):
			sp = super(LocalizedManager, self)
			kwargs['language_attr'] = self.language_attr
			if hasattr(sp, '_construct_query_set'):
				return sp._construct_query_set(cls, *args, **kwargs)
			else:
				return cls(*args, **kwargs)
		
		def get_query_set(self):
			return self._construct_query_set(LocalizedQuerySet, self.model, using=self._db)
		
		def localize(self, language_code=None):
			return self.get_query_set().localize(language_code=language_code)
	
	return LocalizedManager


LocalizedQuerySet = localized_query_set_factory()
LocalizedManager = localized_manager_factory()

