from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    # all patternshave been replaced with a single URL for the view for exchanging a username and password combination for an API token
]
