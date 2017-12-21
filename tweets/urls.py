from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from tweets import views

router = SimpleRouter()
router.register(r'tweets', views.TwitterTweetsView, base_name='tweet')

urlpatterns = [
    url(r'^export-tweets$', views.export_tweet, name='export-tweet'),
]

urlpatterns += router.urls
