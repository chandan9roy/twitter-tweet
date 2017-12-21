import json
import csv
import oauth2

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.files.storage import default_storage
from django.db.models import F, Q
from datetime import datetime
from django.http import HttpResponse

from rest_framework import status, permissions, filters, views, generics, viewsets, mixins
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from tweets.models import Tweet
from tweets.serializers import TweetSerializer


def twitter_oauth_req(url, key, secret, http_method="GET", http_headers=None):
    '''
    Method to authenticate twitter credentials.
    '''
    consumer = oauth2.Consumer(key=settings.TWITTER_API_KEY, secret=settings.TWITTER_API_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, headers=http_headers)
    return content


class TwitterTweetsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    View to get list of tweets.

    **Query Parameters**

    - text
    - text_icontains
    - text_startswith
    - text_endswith
    - created_from
    - created_to
    - created_at
    - group_by
    - order_by
    - page_size

    **Filter Parameter**

    `created_from` - `2016-11-17T07:38:59.523438Z`

    `created_to` - `2016-11-17T07:38:59.523438Z`

    `created_at` - `2016-11-17T07:38:59.523438Z`

    `group_by` - [`text`, 'created_at']

    `order_by` - [`text`, 'created_at']

    `page_size` - 100

    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def filter_queryset(self, queryset):
        queryset = super(TwitterTweetsView, self).filter_queryset(queryset)

        text = self.request.query_params.get('text')
        text_icontains = self.request.query_params.get('text_icontains')
        text_startswith = self.request.query_params.get('text_startswith')
        text_endswith = self.request.query_params.get('text_endswith')

        created_from = self.request.query_params.get('created_from')
        created_at = self.request.query_params.get('created_at')
        created_to = self.request.query_params.get('created_to')

        group_by = self.request.query_params.get('group_by')
        page_size = self.request.query_params.get('page_size', 100)

        order_by = self.request.query_params.get('order_by')

        if text:
            queryset = queryset.filter(text=text)

        elif text_icontains:
            queryset = queryset.filter(text__icontains=text_icontains)

        elif text_startswith:
            queryset = queryset.filter(text__startswith=text_startswith)

        elif text_endswith:
            queryset = queryset.filter(text__endswith=text_endswith)

        else:
            pass

        if created_from:
            queryset = queryset.filter(created_at__gte=created_from)

        if created_to:
            queryset = queryset.filter(created_at__lte=created_to)

        if created_at:
            queryset = queryset.filter(created_at=created_at)

        if group_by in ['text', 'created_at']:
            queryset = queryset.annotate(field_name=F(group_by)).order_by('field_name')

        if order_by in ['text', 'created_at']:
            queryset = queryset.order_by(order_by)

        return queryset


def get_twitter_tweets(search_text, page_size=1000):
    url = settings.TWITTER_API + '?q=%23'+ search_text + '&count=' + str(page_size) +'&result_type=mixed&lang=en'
    tweets = twitter_oauth_req(url, settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    tweets = json.loads(tweets.decode("utf-8"))
    statuses = tweets.get('statuses', [])
    twitter_text_list = []

    for stat in statuses:
        created_time = datetime.strptime(stat['created_at'], '%a %b %d %H:%M:%S %z %Y')
        twitter_text_list.append(Tweet(
             text=stat['text'], created_by_image=stat['user']['profile_image_url'], created_by_name=stat['user']['name'],
             created_at=created_time, url='https://twitter.com/'+ stat['user']['screen_name'] +'/status/' + stat['id_str']
            )
        )

    Tweet.objects.bulk_create(twitter_text_list)


def export_tweet(request):

    queryset = Tweet.objects.all()
    text = request.GET.get('text')
    text_icontains = request.GET.get('text_icontains')
    text_startswith = request.GET.get('text_startswith')
    text_endswith = request.GET.get('text_endswith')

    created_from = request.GET.get('created_from')
    created_at = request.GET.get('created_at')
    created_to = request.GET.get('created_to')

    if text:
        queryset = queryset.filter(text=text)

    elif text_icontains:
        queryset = queryset.filter(text__icontains=text_icontains)

    elif text_startswith:
        queryset = queryset.filter(text__startswith=text_startswith)

    elif text_endswith:
        queryset = queryset.filter(text__endswith=text_endswith)

    else:
        pass

    if created_from:
        queryset = queryset.filter(created_at__gte=created_from)

    if created_to:
        queryset = queryset.filter(created_at__lte=created_to)

    if created_at:
        queryset = queryset.filter(created_at=created_at)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tweet.csv"'

    writer = csv.writer(response)

    for obj in queryset:
        text = obj.text.replace(';', ' ')
        writer.writerow([text, obj.created_by_image, obj.created_by_name, obj.url, obj.created_at])

    return response
