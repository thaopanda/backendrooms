from Post.models import Post
from Account.models import Renter
from Review.models import Review
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator

rating_validator = ('^[1-5]{1}$')
comment_validator = ('^[a-zA-zÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9\s]+$')
class CreateReviewView(APIView):
    class CreateReviewSerializer(serializers.ModelSerializer):
        rating = serializers.IntegerField(validators=[RegexValidator(regex=rating_validator)])
        comment = serializers.CharField(validators=[RegexValidator(regex=comment_validator)])
        class Meta:
            model = Review
            fields = ['id', 'rating', 'comment']
    
    def post(self, request,pk, format=None):
        serializer = self.CreateReviewSerializer(data=request.data)
        if(serializer.is_valid()):
            user = Renter.objects.get(email=request.user.email)
            post = Post.objects.get(pk=pk)
            serializer.save(renter_id=user, post_id=post)
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

    def get(self, request, pk, begin, end, format=None):
        reviewList = Review.objects.filter(post_id=pk, is_confirmed=True)[begin:end]
        serializer = self.ListReviewOfPostSerializer(reviewList, many=True)
        response = {
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)

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

#for admin
class ListReview(APIView):
    permission_classes = (IsAuthenticated,)
    class ListReviewOfRenterSerializer(serializers.ModelSerializer):
        post_id = serializers.SlugRelatedField(read_only=True,slug_field='detailAddress')
        class Meta:
            model = Review
            fields = ['id','post_id', 'rating', 'comment']

    def get(self, request, format=None):
        reviewList = Review.objects.filter(is_confirmed=False)
        serializer = self.ListReviewOfRenterSerializer(reviewList, many=True)
        return Response(serializer.data)


class ConfirmReview(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request,pk, format=None):
        review = Review.objects.get(pk=pk)
        review.is_confirmed = True
        review.save()
        return Response(f'ok')