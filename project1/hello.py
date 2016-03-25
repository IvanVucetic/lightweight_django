from django.conf import settings

from django.conf.urls import url
from django.http import HttpResponse

settings.configure(
	DEBUG=True,
	SECRET_KEY='thisisthesecretkey', #in production should actually be random
	ROOT_URLCONF=__name__,
	MIDDLEWARE_CLASSES=(
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
)

def index(request):
	return HttpResponse('Hello World!')


urlpatterns = (
	url(r'^$', index),
)
