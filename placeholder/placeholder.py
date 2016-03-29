import hashlib
import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', '^8vc1a3t3umr+gpghe#srsvwlt&=#q7z=u%f-!=^!fzz3bw7@i')

BASE_DIR = os.path.dirname(__file__)

settings.configure(
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY, #in production should actually be random
	ROOT_URLCONF=__name__,
	MIDDLEWARE_CLASSES=(
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
	INSTALLED_APPS = (
		'django.contrib.staticfiles',
	),
	TEMPLATE_DIRS = (
		os.path.join(BASE_DIR, 'templates'),
	),
	STATICFILES_DIRS = (
		os.path.join(BASE_DIR, 'static'),
	),
	STATIC_URL = '/static/',
)

#import forms for validation of url parametars
from django import forms
#definition of URLS
from django.conf.urls import url
# enable caching
from django.core.cache import cache
#creation of WSGI application
from django.core.wsgi import get_wsgi_application
#http response generation
from django.http import HttpResponse, HttpResponseBadRequest
# etag decorator for utilization of browser cache
from django.views.decorators.http import etag

# image generation requirements
from io import BytesIO
from PIL import Image. ImageDraw

class Imageform(forms.Form):
	"""Form to validate requested placeholder image."""

	height = forms.IntegerField(min_value=1, max_value=2000)
	width = forms.IntegerField(min_value=1, max_value=2000)

	def generate(self, image_format='PNG'):
		"""Generate an image of the given type and and return as raw bytes"""
		height = self.cleaned_data['height']
		width = self.cleaned_data['width']
		key = '{}.{}.{}'.format(width, height, image_format)
		content = cache.get(key)
		if content is None:
			image = Image.new('RGB', (width, height))
			draw = ImageDraw.Draw(image)
			text = '{} x {}'.format(width, height)
			textwidth, textheight = draw.textsize(text)
			if textwidth < width and textheight < height:
				texttop = (height - textheight) // 2
				textleft = (width - textwidth) // 2
				draw.text((textleft, texttop), text, fill=(255, 255, 255))
			content = BytesIO()
			image.save(content, image_format)
			content.seek(0)
			cache.set(key, content, 60 * 60) #cache time 1hr
		return content

def generate_etag(request, width, height):
	content = 'placeholder: {0} x {1}'.format(width, height)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
	form = Imageform({'height':height, 'width':width})
	if form.is_valid():
		image = form.generate()
		return HttpResponse(image, content_type='image/png')
	else:
		return HttpResponseBadRequest('Invalid Image Request')


def index(request):
	return HttpResponse('Hello World!')

#named groups are captured using the ?P syntax and passed as keyword arguments
urlpatterns = (
	#incoming requests to the URL /image/30x25/ will be routed to the placeholder
	#view and pass in those values (e.g., width=30 and height=25 )
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
	url(r'^$', index, name='homepage'),
)

# Create WSGI application - needed to communicate with normal web server
application = get_wsgi_application()

if __name__=="__main__":
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
