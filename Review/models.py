from django.db import models
from Account.models import Renter
from Post.models import Post

class Review(models.Model):
    renter_id = models.ForeignKey(Renter, related_name='renter_review', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='post_review', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    date_review = models.DateTimeField(auto_now_add=True, verbose_name='date review')