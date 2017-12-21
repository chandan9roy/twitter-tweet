from rest_framework import serializers
from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('text', 'created_by_name', 'created_by_image', 'url', 'created_at')
