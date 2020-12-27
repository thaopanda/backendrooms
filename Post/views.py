from Post.models import Post
from Account.models import Host, MyUser
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator
from EasyAccomd.permissions import ViewAndChangePermission, IsRenter
from datetime import datetime, timedelta, timezone, tzinfo

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
        images = serializers.CharField()
        class Meta:
            model = Post
            fields = ['detailAddress', 'describeAddress', 
            'roomType', 'numberOfRoom', 'price', 'rent_time' ,'square', 'withOwner',
            'bathroomType', 'heater','kitchen', 'airconditioner', 'balcony',
            'water_price','electricity_price', 'other', 'numberOfRented', 'images']
    def put(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        if(post.is_confirmed is False):
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
            fields = ['id','is_confirmed','images','detailAddress', 'numberOfRoom','hostName']
    def get(self, request, format=None):
        hostPostList = Post.objects.filter(hostName=request.user)
        serializer = self.HostPostListSerializer(hostPostList, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
        # serializer.data['images']=transformToArray(serializer.data['images'])
        response = {
            'data':serializer.data,
            # 'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)

class PostDetailView(APIView):
    class PostDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'
    
    def get(self, request, pk, format=None):
        postDetail = Post.objects.filter(pk=pk)
        serializer = self.PostDetailSerializer(postDetail, many=True)
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data[0],
        }
        return Response(response)
class SearchByCiteria(APIView):
    class SearchSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['id','detailAddress', 'hostName', 'images']

    def get(self, request, address, describeAddress, price, roomType, square, kitchen, bathroom, heater, airconditioner, begin, end, format=None):
        result = Post.objects.filter(
            detailAddress__contains=address,
            describeAddress__contains= describeAddress,
            price=price,
            roomType=roomType,
            square=square,
            kitchen=kitchen,
            bathroomType=bathroom,
            heater=heater,
            airconditioner=airconditioner
        )[begin:end]
        serializer = self.SearchSerializer(result, many=True)
        # host = Host.objects.get(pk=serializer.data['hostName'])
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)
    
class Search(APIView):
    class SearchSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['id','detailAddress', 'hostName', 'images']
    
    def get(self, request, searching, begin, end, format=None):
        result = Post.objects.filter(detailAddress__contains=searching)[begin:end]
        serializer = self.SearchSerializer(result, many=True)

        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
        }
        return Response(response)
        
class HomePageView(APIView):
    class HomePageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ['detailAddress','id','hostName', 'images']
    
    def get(self, request, location, begin, end, format=None):
        result = Post.objects.filter(detailAddress__contains=location)[begin:end]
        serializer = self.HomePageSerializer(result, many=True)
        
        for i in serializer.data:
            i['images']=transformToArray(i['images'])
            i['hostName']=Host.objects.get(pk=i['hostName']).fullname 

        response = {
            # 'host':host.fullname,
            'data':serializer.data,
            'hasNext':len(serializer.data)==end-begin
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
            serializer.save()
            return Response(f'ok')
        return Response(f'not ok')


