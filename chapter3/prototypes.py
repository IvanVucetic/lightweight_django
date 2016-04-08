import os
import sys

from django.conf import settings

SECRET_KEY = os.environ.get('SECRET_KEY', 'b=s36a+rw@)r7vwbn8(qs90-2spyksh$m8g286$!tw01%bwrde')

BASE_DIR = os.path.dirname(__file__)

settings.configure(
	DEBUG=True,
	SECRET_KEY=SECRET_KEY, #in production should actually be random
	ROOT_URLCONF='sitebuilder.urls',
	MIDDLEWARE_CLASSES=(),
	INSTALLED_APPS=(
		'django.contrib.staticfiles',
		'django.contrib.webdesign', #creates placeholder text (lorem ipsum)
		'sitebuilder',
		'compressor',
	),
	STATIC_URL='/static/',
	SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR, 'pages'),
	SITE_OUTPUT_DIRECTORY = os.path.join(BASE_DIR, '_build'),
	STATIC_ROOT = os.path.join(BASE_DIR, '_build', 'static'),
	STATICFILES_FINDERS = (
		'django.contrib.staticfiles.finders.FileSystemFinder',
		'django.contrib.staticfiles.finders.AppDirectoriesFinder',
		'compressor.finders.CompressorFinder',	
	),
)


if __name__=="__main__":
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
