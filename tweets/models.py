from django.db import models


class Tweet(models.Model):
    """
    Stores information of twitter tweets.
    """
    text = models.TextField()
    created_by_image = models.CharField(max_length=255)
    created_by_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at= models.DateTimeField()

    def __str__(self):
        return "{id} - {url}".format(id=self.id, url=self.url)
