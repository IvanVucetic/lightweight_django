import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ secret_key }}')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY, #in production should actually be random
	ALLOWED_HOSTS=ALLOWED_HOSTS,
	ROOT_URLCONF=__name__,
	MIDDLEWARE_CLASSES=(
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
)


#definition of URLS
from django.conf.urls import url
#creation of WSGI application
from django.core.wsgi import get_wsgi_application
#http response generation
from django.http import HttpResponse

def index(request):
	return HttpResponse('Hello World!')


urlpatterns = (
	url(r'^$', index),
)

# Create WSGI application - needed to communicate with normal web server
application = get_wsgi_application()

if __name__=="__main__":
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
