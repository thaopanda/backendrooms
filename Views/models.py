from django.db import models
from Post.models import Post


class ViewsManager(models.Manager):
    def createView(self, post):
        view = self.model(post=post)
        view.save(using = self._db)
        return view

class Views(models.Model):
    post = models.ForeignKey(Post, related_name='view_post', on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)
    objects = ViewsManager()