from setuptools import setup, find_packages

setup(
    name = "django_i18n_attrhelpers",
    version = "0.1.1-2",
    description = 'Helpers for accessing ..._$LANG-fields',
    author = 'David Danier',
    author_email = 'david.danier@team23.de',
    url = 'https://github.com/ddanier/django_i18n_attrhelpers',
    #long_description=open('README.rst', 'r').read(),
    packages = [
        'django_i18n_attrhelpers',
    ],
    package_data = {
        'django_i18n_attrhelpers': ['locale/*/LC_MESSAGES/*'],
    },
    install_requires = [
        'Django >=1.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)

