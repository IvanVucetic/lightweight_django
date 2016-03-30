import os
import sys

from django.conf import settings

SECRET_KEY = os.environ.get('SECRET_KEY', 'b=s36a+rw@)r7vwbn8(qs90-2spyksh$m8g286$!tw01%bwrde')

settings.configure(
	DEBUG=True,
	SECRET_KEY=SECRET_KEY, #in production should actually be random
	ROOT_URLCONF='sitebuilder.urls',
	MIDDLEWARE_CLASSES=(),
	INSTALLED_APPS=(
		'django.contrib.staticfiles',
		'django.contrib.webdesign', #creates placeholder text (lorem ipsum)
		'sitebuilder',
	),
	STATIC_URL='/static/',
)


if __name__=="__main__":
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
