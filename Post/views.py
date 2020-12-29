from Post.models import Post
from Views.models import Views
from Favorite.models import Favorite
from Account.models import Host, MyUser
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator
from EasyAccomd.permissions import ViewAndChangePermission, IsRenter
from datetime import datetime, timedelta, timezone, tzinfo
import django_filters
from rest_framework import generics
from django_filters import rest_framework as rf

detailAddress_validator=('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')
describeAddress_validator=('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')
other_validator=('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')


ROOM_TYPE = [
    ('phòng trọ', "phòng trọ"),
    ('chung cư mini', "chung cư mini"),
    ('nhà nguyên căn', "nhà nguyên căn"),
    ('chung cư nguyên căn', "chung cư nguyên căn")
]

RENT_TIME = [
    ('tháng', 'tháng'),
    ('quý', 'quý'),
    ('năm', 'năm'),
]

BATH_ROOM = [
    ('khép kín', "khép kín"),
    ('chung', "chung")
]
KITCHEN = [
    ('khu bếp riêng', "khu bếp riêng"),
    ('khu bếp chung', "khu bếp chung"),
    ('không nấu ăn', "không nấu ăn")
]

def transformToString(images_Array):
    images_string=''
    for i in images_Array:
        images_string+=i+'&'
    return(images_string)

def transformToArray(images_string):
    images_array = images_string.split("&")
    images_array.pop(len(images_array)-1)
    return images_array

class CreatePostView(APIView):
    permission_classes = (IsRenter,)
    class CreatePostSerializer(serializers.ModelSerializer):
        hostName =serializers.SlugRelatedField(read_only=True, slug_field='fullname', many=True)
        detailAddress = serializers.CharField(
            validators=[RegexValidator(regex=detailAddress_validator)]
        )
        describeAddress = serializers.CharField(
            validators=[RegexValidator(regex=describeAddress_validator)]
        )
        roomType = serializers.ChoiceField(choices=ROOM_TYPE)
        numberOfRoom = serializers.IntegerField()
        price = serializers.IntegerField()
        rent_time = serializers.ChoiceField(choices=RENT_TIME)
        square = serializers.IntegerField()
        withOwner = serializers.BooleanField()
        bathroomType = serializers.ChoiceField(choices=BATH_ROOM)
        heater = serializers.BooleanField()
        kitchen = serializers.ChoiceField(choices=KITCHEN)
        airconditioner =serializers.BooleanField()
        balcony = serializers.BooleanField()
        water_price = serializers.IntegerField()
        electricity_price = serializers.IntegerField()
        other = serializers.CharField(
            validators=[RegexValidator(regex=other_validator)]
        )
        # images = serializers.CharField()
        expiredDate = serializers.IntegerField()
        class Meta:
            model = Post
            fields = ['id', 'detailAddress', 'describeAddress', 
            'roomType', 'numberOfRoom', 'price', 'rent_time', 'square', 'withOwner',
            'bathroomType','heater', 'kitchen', 'airconditioner', 'balcony',
            'water_price','electricity_price', 'other', 'hostName', 
            'is_confirmed', 'numberOfRented','expiredDate']
    

    def post(self, request, format=None):
        serializer = self.CreatePostSerializer(data=request.data)
        print(serializer.initial_data)
        if(serializer.is_valid()):
            
            images = serializer.initial_data['images']
            print(images)
            serializer.validated_data['images']=transformToString(images)
            user = Host.objects.get(email=request.user.email)
            serializer.save(hostName=user, is_confirmed=False, numberOfRented=0, expiredDate = datetime.now()+timedelta(days=serializer.validated_data['expiredDate']))
            return Response(f'ok')
        return Response(f'not ok')

class UpdatePostView(APIView):
    # permission_classes = (ViewAndChangePermission,)
    class UpdatePostSerializer(serializers.ModelSerializer):
        detailAddress = serializers.CharField(
            validators=[RegexValidator(regex=detailAddress_validator)]
        )
        describeAddress = serializers.CharField(
            validators=[RegexValidator(regex=describeAddress_validator)]
        )
        roomType = serializers.ChoiceField(choices=ROOM_TYPE)
        numberOfRoom = serializers.IntegerField()
        price = serializers.IntegerField()
        # rent_time = serializers.ChoiceField(choices=RENT_TIME)
        square = serializers.IntegerField()
        withOwner = serializers.BooleanField()
        bathroomType = serializers.ChoiceField(choices=BATH_ROOM)
        heater = serializers.BooleanField()
        kitchen = serializers.ChoiceField(choices=KITCHEN)
        airconditioner =serializers.BooleanField()
        balcony = serializers.BooleanField()
        water_price = serializers.IntegerField()
        electricity_price = serializers.IntegerField()
        other = serializers.CharField(
            validators=[RegexValidator(regex=other_validator)]
        )
        # images = serializers.CharField()
        class Meta:
            model = Post
            fields = ['detailAddress', 'describeAddress', 
            'roomType', 'numberOfRoom', 'price' ,'square', 'withOwner',
            'bathroomType', 'heater','kitchen', 'airconditioner', 'balcony',
            'water_price','electricity_price', 'other']
    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        if(post.is_confirmed is False):
            print('ok')
            serializer = self.UpdatePostSerializer(post, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(f'ok')
        return Response(f'not ok')

class UpdateRentStatusView(APIView):
    # permission_classes = (ViewAndChangePermission,)
    class UpdateRentStatusSerializer(serializers.ModelSerializer):
        numberOfRented = serializers.IntegerField()
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

class ExtendExpiredDateView(APIView):
    class ExtendExpiredDateSerializer(serializers.ModelSerializer):
        expiredDate = serializers.IntegerField()
        class Meta:
            model = Post
            fields = ['expiredDate']
    
    def put(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)
        if(post.expiredDate.replace(tzinfo=None)<datetime.now().replace(tzinfo=None)):
            serializer = self.ExtendExpiredDateSerializer(post, data=request.data)
            if(serializer.is_valid()):
                serializer.save(is_confirmed=False, expiredDate = datetime.now()+timedelta(days=serializer.validated_data['expiredDate']))
                return(Response(f'ok'))
            return Response(f'serializer not valid')
        return Response(f'this post has not expired yet')

class HostPostListView(APIView):
    class HostPostListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['id','is_confirmed','images','detailAddress', 'numberOfRoom', 'numberOfRoom', 'total_like', 'total_views']
    def get(self, request, format=None):
        hostPostList = Post.objects.filter(hostName=request.user)
        serializer = self.HostPostListSerializer(hostPostList, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
        response = {
            'data':serializer.data,
        }
        return Response(response)

class PostDetailView(APIView):
    permission_classes = (AllowAny,)
    class PostDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
    
    def get(self, request, pk, format=None):
        postDetail = Post.objects.filter(pk=pk)
        favorite = Favorite.objects.filter(renter_id=request.user, post_id=postDetail[0])
        print(favorite)
        liked = False
        if(len(favorite)!=0):
            liked = True

        total_view = 0
        serializer = self.PostDetailSerializer(postDetail, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 
            i['total_views']=i['total_views']+1
            total_view = i['total_views']
        if(request.user.is_anonymous or request.user.user_type=='renter'):
            Views.objects.createView(postDetail[0])
            postDetail[0].total_views = total_view
            postDetail[0].save()

        response = {
            # 'host':host.fullname,
            'data':serializer.data[0],
            'liked':liked
        }
        return Response(response)
    
class Search(APIView):
    class SearchSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['detailAddress','id', 'images', 'total_like', 'total_views']
    
    def get(self, request, searching, begin, end, format=None):
        result = Post.objects.filter(detailAddress__contains=searching)[begin:end]
        serializer = self.SearchSerializer(result, many=True)

        for i in serializer.data:
            i['images']=transformToArray(i['images'])

        response = {
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)
        
class HomePageView(APIView):
    permission_classes = (AllowAny,)
    class HomePageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['detailAddress','id', 'images', 'total_like', 'total_views']
    
    def get(self, request, location, begin, end, format=None):
        result = Post.objects.filter(detailAddress__contains=location)[begin:end]
        serializer = self.HomePageSerializer(result, many=True)
        
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
        response = {
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)
        
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['detailAddress','id', 'images', 'total_like', 'total_views']

class SearchFilter(django_filters.FilterSet):
    detailAddress = django_filters.CharFilter(field_name='detailAddress', lookup_expr='icontains')
    describeAddress = django_filters.CharFilter(field_name='describeAddress', lookup_expr='icontains')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    square = django_filters.NumberFilter(field_name='square', lookup_expr='gte')
    class Meta:
        model = Post
        fields = ['detailAddress', 'describeAddress', 'price', 'roomType', 'square', 'kitchen', 'bathroomType', 'heater', 'airconditioner']

class SearchByCiteria(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    filterset_class = SearchFilter
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            # i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data,
            # 'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)


# for admin only

class ConfirmedPost(APIView):
    class ConfirmedPostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['is_confirmed']
    
    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        serializer = self.ConfirmedPostSerializer(post, data=request.data)
        if(serializer.is_valid()):
            serializer.save(is_confirmed=True)
            return Response(f'ok')
        return Response(f'not ok')


class PostList(APIView):
    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
    def get(self, request,confirm,begin, end, format=None):
        postDetail = Post.objects.filter(is_confirmed=confirm)[begin:end]
        serializer = self.PostSerializer(postDetail, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data,
        }
        return Response(response)
