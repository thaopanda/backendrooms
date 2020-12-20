from rest_framework import serializers
from Account.models import MyUser, Host, Renter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from EasyAccomd.permissions import ViewAndChangePermission, IsOwner, IsRenter, IsHost
from datetime import datetime, timedelta

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

username_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9_\s]+$')
email_validator = ('^[a-zA-Z0-9]+@[a-zA-Z.]+$')
fullname_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ\s]+$')
identication_validator =('^[0-9]{12}$')
phoneNumber_validator = ('^[0]{1}[0-9]{9}$')
address_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')
interested_area_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')


class RenterRegistrationView(APIView):
    permission_classes = (AllowAny,)
    class RenterRegistrationSerializer(serializers.ModelSerializer):
        username = serializers.CharField(
            max_length=30, 
            validators=[UniqueValidator(queryset=MyUser.objects.all()),
                        RegexValidator(regex=username_validator)]
        )
        email = serializers.EmailField(
            validators=[UniqueValidator(queryset=MyUser.objects.all()),
                        RegexValidator(regex=email_validator)],
            max_length=60
        )
        password = serializers.CharField(min_length=8)
        class Meta:
            model = Renter
            fields = ['id', 'email', 'username', 'password']
        
    def post(self, request, format=None):
        serializer = self.RenterRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            Renter.objects.create_user(email=serializer.validated_data['email'], username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            return Response(serializer.data)
        return Response(serializer.errors)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    class LoginViewSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True, min_length=8)
        token = serializers.CharField(max_length=255, read_only=True)
        user_type = serializers.CharField(max_length=10, read_only=True)

        def validate(self, data):
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("user not found")
            if(user.check_password(password) is False):
                raise serializers.ValidationError("password is incorrect")
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            return{
                'email': user.email,
                'token':jwt_token,
                'user_type':user.user_type,
            }
    def post(self, request, format=None):
        serializer = self.LoginViewSerializer(data=request.data)
        if(serializer.is_valid()):
            response = {
            'success' : 'True',
            'message': 'User logged in  successfully',
            'email': serializer.data['email'],
            'token' : serializer.data['token'],
            'user_type':serializer.data['user_type']
            }
            return Response(response)
        return Response(f'not ok')

class HostRegistrationView(APIView):
    permission_classes = (AllowAny,)
    class HostRegistrationSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(
            validators=[RegexValidator(regex=email_validator)]
        )
        username = serializers.CharField(
            validators=[RegexValidator(regex=username_validator)]
        )
        password = serializers.CharField(min_length=8)
        identication = serializers.CharField(
            validators=[RegexValidator(regex=identication_validator), 
                        UniqueValidator(queryset=Host.objects.all())]
        )
        phoneNumber = serializers.CharField(
            validators=[RegexValidator(regex=phoneNumber_validator), 
                        UniqueValidator(queryset=Host.objects.all())]
        )
        address = serializers.CharField(
            validators=[RegexValidator(regex=address_validator)]
        )
        fullname = serializers.CharField(
            validators=[RegexValidator(regex=fullname_validator)],
            max_length=50
        )
        class Meta:
            model = Host
            fields = ['id', 'email', 'username', 'password', 'fullname', 'identication', 'address', 'phoneNumber']
    def post(self, request, format=None):
        serializer = self.HostRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            Host.objects.create_user(email=serializer.validated_data['email'], 
                                    username=serializer.validated_data['username'], 
                                    password=serializer.validated_data['password'], 
                                    fullname=serializer.validated_data['fullname'], 
                                    identication=serializer.validated_data['identication'], 
                                    address=serializer.validated_data['address'],
                                    phoneNumber=serializer.validated_data['phoneNumber'])
            return Response(serializer.data)
        return Response(serializer.errors)

class RenterProfileView(APIView):
    permission_classes = (IsRenter,)
    
    class RenterProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Renter
            fields = ['username', 'email', 'date_joined', 'last_login', 'fullname', 'interested_area' ]

    def get(self, request, format=None):
        print(request.user.email)
        Profile = Renter.objects.get(email=request.user.email)
        serializer = self.RenterProfileSerializer(Profile)
        return Response(serializer.data)

class HostProfileView(APIView):
    permission_classes = (IsHost,)
    
    class HostProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = ['username', 'email', 'date_joined', 'last_login', 'fullname', 'identication', 'address', 'phoneNumber']

    def get(self, request, format=None):
        print(request.user.email)
        Profile = Host.objects.get(email=request.user.email)
        serializer = self.HostProfileSerializer(Profile)
        return Response(serializer.data)

class RenterUpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,ViewAndChangePermission,)
    class RenterUpdateProfileSerializer(serializers.ModelSerializer):
        fullname = serializers.CharField(
            validators=[RegexValidator(regex=fullname_validator)]
        )
        interested_area = serializers.CharField(
            validators=[RegexValidator(regex=interested_area_validator)]
        )
        class Meta:
            model = Renter
            fields = ['fullname', 'interested_area']
    def put(self, request, format=None):
        renter = Renter.objects.get(email=request.user.email)
        serializer = self.RenterUpdateProfileSerializer(renter, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class HostUpdateProfileView(APIView):
    permission_classes = (IsAuthenticated, ViewAndChangePermission,)
    class HostUpdateProfileSerializer(serializers.ModelSerializer):
        fullname = serializers.CharField(
            required=True,
            validators=[RegexValidator(regex=fullname_validator)]
        )
        identication = serializers.CharField(
            validators=[RegexValidator(regex=identication_validator)]
        )
        phoneNumber = serializers.CharField(
            validators=[RegexValidator(regex=phoneNumber_validator)]
        )
        address = serializers.CharField(
            validators=[RegexValidator(regex=address_validator)]
        )
        class Meta:
            model = Host
            fields = ['fullname', 'identication', 'address', 'phoneNumber']
    
    def put(self, request, format=None):
        host = Host.objects.get(email=request.user.email)
        serializer = self.HostUpdateProfileSerializer(host, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ChangePasswordView(APIView):
    permission_classes = (ViewAndChangePermission,)
    class ChangePasswordSerializer(serializers.ModelSerializer):
        password = serializers.CharField(min_length=8)
        new_password = serializers.CharField(min_length=8)
        class Meta:
            model = MyUser
            fields = ['password', 'new_password']
    def put(self, request, format=None):
        user = MyUser.objects.get(email=request.user.email)
        changePassword = self.ChangePasswordSerializer(user, data=request.data)
        if(changePassword.is_valid()):
            if(user.check_password(changePassword.validated_data['password']) is False):
                return Response(f'incorrect old password')
            if(changePassword.validated_data['password']==changePassword.validated_data['new_password']):
                return Response(f'new password must be different from old password')
            user.set_password(changePassword.validated_data['new_password'])
            user.save()
            return Response(f'ok')
        return Response(f'not ok')

class AllUser(APIView):
    permission_classes = (AllowAny,)
    class AllUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = MyUser
            fields = ['username']

    def get(self, request, begin, end,  format=None):
        profile = MyUser.objects.filter(user_type='renter').order_by("username")[begin:end]
        print(profile)
        serializer = self.AllUserSerializer(profile, many=True)
        response = {
            'data':serializer.data,
            'hasNext': len(serializer.data) == end - begin
        }
        return Response(response)

# class ResetPasswordView(APIView):


#API for admin only
class GetListHost(APIView):
    class ListHostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = ['username', 'email', 'fullname', 'identication', 'address', 'phoneNumber']

    def get(self, request, begin, end, format=None):
        HostList = Host.objects.filter(is_confirmed=True).order_by('date_joined')[begin:end]
        serializer = self.ListHostSerializer(HostList, many=True)
        response = {
            'data':serializer.data,
            'hasNext': len(serializer.data) == end - begin
        }
        return Response(response)

class GetUnconfirmedHost(APIView):
    class UnconfirmedHostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = ['username', 'email', 'fullname', 'identication', 'address', 'phoneNumber']

    def get(self, request, begin, end, format=None):
        HostList = Host.objects.filter(is_confirmed=False).order_by('date_joined')[begin:end]
        serializer = self.UnconfirmedHostSerializer(HostList, many=True)
        response = {
            'data':serializer.data,
            'hasNext': len(serializer.data) == end - begin
        }
        return Response(response)

class ConfirmedHostAccount(APIView):
    class ConfirmedHostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = ['is_confirmed']
    
    def put(self, request, pk, format=None):
        host = Host.objects.get(pk=pk)
        serializer = self.ConfirmedHostSerializer(host, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(f'ok')
        return Response(f'not ok')

class AllowUpdatePermission(APIView):
    class AllowUpdatePermissionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = ['has_update_permission']
    
    def put(self, request, pk, format=None):
        host = Host.objects.get(pk=pk)
        serializer = self.AllowUpdatePermissionSerializer(host, data=request.data)
        if(serializer.is_valid()):
            serializer.save(is_confirmed=False)
            return Response(f'ok')
        return Response(f'not ok')

