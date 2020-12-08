from Post.models import Post
from Account.models import Host, MyUser
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class CreatePostView(APIView):
    class CreatePostSerializer(serializers.ModelSerializer):
        host_id = serializers.PrimaryKeyRelatedField(queryset=Host.objects.all(), many=True)
        hostName =serializers.CharField(read_only=True)
        hostPhoneNumber = serializers.CharField(read_only=True)
        class Meta:
            model = Post
            fields = ['id', 'detailAddress', 'describeAddress', 
            'roomType', 'numberOfRoom', 'price', 'square', 'withOwner',
            'bathroomType', 'kitchen', 'airconditioner', 'balcony',
            'utility', 'other', 'host_id', 'hostName', 'hostPhoneNumber', 
            'is_confirmed', 'numberOfRented']
    
    def post(self, request, format=None):
        serializer = self.CreatePostSerializer(data=request.data)
        if(serializer.is_valid()):
            user = Host.objects.get(email=request.user.email)
            serializer.save(host_id = user, hostName=user.fullname, hostPhoneNumber=user.phoneNumber, is_confirmed=False, numberOfRented=0)
            return Response(f'ok')
        return Response(f'not ok')

class UpdatePostView(APIView):
    class UpdatePostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['detailAddress', 'describeAddress', 
            'roomType', 'numberOfRoom', 'price', 'square', 'withOwner',
            'bathroomType', 'kitchen', 'airconditioner', 'balcony',
            'utility', 'other']
    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        if(post.is_confirmed is False):
            serializer = self.UpdatePostSerializer(post, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(f'ok')
        return Response(f'not ok')

class UpdateRentStatusView(APIView):
    class UpdateRentStatusSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['numberOfRented']

    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        if(post.is_confirmed is True):
            serializer = self.UpdateRentStatusSerializer(post, data=request.data)
            if(serializer.is_valid()):
                availableRoom = post.numberOfRoom - serializer.validated_data['numberOfRented']
                if(availableRoom>=0):
                    serializer.save(numberOfRoom = availableRoom)
                    return Response(f'ok')
        return Response(f'not ok')

# class ExtendExpiredDateView(APIView):

class HostPostListView(APIView):
    class HostPostListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['detailAddress', 'numberOfRoom']
    def get(self, request, format=None):
        hostPostList = Post.objects.filter(host_id=request.user)
        serializer = self.HostPostListSerializer(hostPostList, many=True)
        return Response(serializer.data)

class PostDetailView(APIView):
    class PostDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
    
    def get(self, request, pk, format=None):
        postDetail = Post.objects.get(pk=pk)
        serializer = self.PostDetailSerializer(postDetail)
        return Response(serializer.data)

# class SearchByCiteria(APIView):