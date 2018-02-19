#!/usr/bin/env python
from distutils.core import setup
from payu import get_version
import os

setup(name='django-payu',
      version=get_version().replace(' ', '-'),
      description='PayU Payment Gateway integration package for Django',
      author='PayU India',
      author_email='care@payu.in',
      url='http://www.payu.in/',
      packages=['payu'],
      package_data={'payu': ['templates/payu_form.html']},
     )