from Post.models import Post
from Account.models import Renter
from Favorite.models import Favorite
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

def transformToArray(images_string):
    images_array = images_string.split("&")
    images_array.pop(len(images_array)-1)
    return images_array

class CreateAndDeleteFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request,pk, format=None):
        user = Renter.objects.get(email=request.user.email)
        post = Post.objects.get(pk=pk)
        favorite = Favorite.objects.filter(renter_id=user, post_id=post)
        if(len(favorite)!=0):
            post.total_like = post.total_like-1
            post.save()
            favorite[0].delete()
        else:
            post.total_like = post.total_like+1
            post.save()
            Favorite.objects.createFavorite(user,post)
        return Response(f'ok')


class FavoriteList(APIView):
    permission_classes = (IsAuthenticated,)
    class FavoriteListSerializer(serializers.ModelSerializer):
        post_id = serializers.SlugRelatedField(read_only=True,slug_field='id')
        class Meta:
            model = Favorite
            fields = ['post_id']

    class PostInformationSerializer(serializers.ModelSerializer):
        hostName = serializers.SlugRelatedField(read_only=True, slug_field='fullname')
        detailAddress = serializers.CharField(read_only=True)
        class Meta:
            model = Post
            fields = ['id','hostName', 'detailAddress', 'images']

    def get(self, request, begin, end, format=None):
        favoriteList = Favorite.objects.filter(renter_id=request.user)[begin:end]
        serializer = self.FavoriteListSerializer(favoriteList, many=True)
        result = []
        for i in serializer.data:
            postInfor = Post.objects.get(pk= i['post_id'])
            infor = self.PostInformationSerializer(postInfor)
            result.append(infor.data)
        for i in result:
            i['images'] = transformToArray(i['images'])
        response ={
            'data':result,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)

class FavoriteCountView(APIView):
    def get(self,request, pk, format=None):
        count = Favorite.objects.filter(post_id=pk).count()
        response ={
            'count':count
        }
        return Response(response)