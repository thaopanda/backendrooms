from django.db import models
from Account.models import Renter
from Post.models import Post

class Report(models.Model):
    renter_id = models.ForeignKey(Renter, related_name='renter_report', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='post_report', on_delete=models.CASCADE)
    reason = models.TextField()
    is_confirmed = models.BooleanField()
    date_report = models.DateTimeField(auto_now_add=True)
