from Post.models import Post
from Account.models import Renter
from Favorite.models import Favorite
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    class CreateFavoriteSerializer(serializers.ModelSerializer):
        renter_id = serializers.PrimaryKeyRelatedField(queryset=Renter.objects.all(), many=True)
        post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=False)
        class Meta:
            model = Favorite
            fields = ['renter_id', 'post_id']
    
    def post(self, request, format=None):
        serializer = self.CreateFavoriteSerializer(data=request.data)
        if(serializer.is_valid()):
            user = Renter.objects.get(email=request.user.email)
            serializer.save(renter_id=user)
            return Response(f'ok')
        return Response(f'not ok')

class DeleteFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, pk,format=None):
        favorite = Favorite.objects.get(renter_id=request.user.id, post_id=pk)
        favorite.delete()
        return Response(f'ok')

class FavoriteList(APIView):
    permission_classes = (IsAuthenticated,)
    class FavoriteListSerializer(serializers.ModelSerializer):
        post_id = serializers.SlugRelatedField(read_only=True,slug_field='detailAddress')
        class Meta:
            model = Favorite
            fields = ['post_id']

    def get(self, request, begin, end, format=None):
        favoriteList = Favorite.objects.filter(renter_id=request.user)[begin:end]
        serializer = self.FavoriteListSerializer(favoriteList, many=True)
        response ={
            'data':serializer.data,
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