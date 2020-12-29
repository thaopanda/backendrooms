from django.db import models
from Account.models import Renter
from Post.models import Post

class FavoriteManager(models.Manager):
    def createFavorite(self, renter, post):
        favo = self.model(renter_id=renter, post_id=post)
        favo.save(using = self._db)
        return(favo)

class Favorite(models.Model):
    renter_id = models.ForeignKey(Renter, related_name='renter', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    
    objects = FavoriteManager()
