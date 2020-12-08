from Post.models import Post
from Account.models import Renter
from Review.models import Review
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreateReviewView(APIView):
    class CreateReviewSerializer(serializers.ModelSerializer):
        renter_id = serializers.PrimaryKeyRelatedField(queryset=Renter.objects.all(), many=True)
        post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=False)
        class Meta:
            model = Review
            fields = ['renter_id', 'post_id', 'rating', 'comment']
    
    def post(self, request, format=None):
        serializer = self.CreateReviewSerializer(data=request.data)
        if(serializer.is_valid()):
            user = Renter.objects.get(email=request.user.email)
            serializer.save(renter_id=user)
            return Response(f'ok')
        return Response(f'not ok')

class DeleteReviewView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, pk,format=None):
        favorite = Review.objects.get(renter_id=request.user.id, post_id=pk)
        favorite.delete()
        return Response(f'ok')

class ListReviewOfPost(APIView):
    class ListReviewOfPostSerializer(serializers.ModelSerializer):
        renter_id = serializers.SlugRelatedField(read_only=True,slug_field='username')
        class Meta:
            model = Review
            fields = ['renter_id', 'rating', 'comment']

    def get(self, request, pk, format=None):
        reviewList = Review.objects.filter(post_id=pk, is_confirmed=True)
        serializer = self.ListReviewOfPostSerializer(reviewList, many=True)
        return Response(serializer.data)

class ListReviewOfRenter(APIView):
    permission_classes = (IsAuthenticated,)
    class ListReviewOfRenterSerializer(serializers.ModelSerializer):
        post_id = serializers.SlugRelatedField(read_only=True,slug_field='detailAddress')
        class Meta:
            model = Review
            fields = ['post_id', 'rating', 'comment']

    def get(self, request, format=None):
        reviewList = Review.objects.filter(renter_id=request.user)
        serializer = self.ListReviewOfRenterSerializer(reviewList, many=True)
        return Response(serializer.data)