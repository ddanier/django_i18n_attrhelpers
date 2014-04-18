from django.utils.translation import get_language
from django.conf import settings


class I18NAttributeDescriptor(object):
	def __init__(self, options, name):
		self.options = options
		self.name = name
	
	def _languages(self):
		cur = get_language()
		if self.options.fallback_languages is None:
			return [cur] + [l[0] for l in settings.LANGUAGES if l[0] != cur]
		else:
			return [cur] + list(self.options.fallback_languages)
	
	def _language_attribute(self, language):
		return '%s_%s' % (self.name, language)
	
	def __get__(self, obj, type=None):
		if obj is None:
			raise AttributeError('%s is only accessible on instances' % self.name)
		for lang in self._languages():
			value = getattr(obj, self._language_attribute(lang), None)
			if value is not None:
				return value
		return None
	
	def __set__(self, obj, value):
		setattr(obj, self._language_attribute(get_language()), value)


class I18NAttribute(object):
	# pass [] as fallback_languages to disable fallbacks
	def __init__(self, fallback_languages=None):
		self.fallback_languages = fallback_languages
	
	def contribute_to_class(self, model, name):
		setattr(model, name, I18NAttributeDescriptor(self, name))
		if not hasattr(model, '_i18n_attributes'):
			model._i18n_attributes = []
		model._i18n_attributes.append(name)

