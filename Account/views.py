from rest_framework import serializers
from Account.models import MyUser, Host, Renter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class RenterRegistrationView(APIView):
    permission_classes = (AllowAny,)
    class RenterRegistrationSerializer(serializers.ModelSerializer):
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
        email = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)
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
    permission_classes = (IsAuthenticated,)
    
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
    permission_classes = (IsAuthenticated,)
    
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
    class RenterUpdateProfileSerializer(serializers.ModelSerializer):
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
    class HostUpdateProfileSerializer(serializers.ModelSerializer):
        # fullname = serializers.CharField(required=True)
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
    permission_classes = (IsAuthenticated,)
    class ChangePasswordSerializer(serializers.ModelSerializer):
        password = serializers.CharField()
        new_password = serializers.CharField()
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
        Profile = MyUser.objects.filter(user_type='renter').order_by("username")[begin:end]
        print(Profile)
        serializer = self.AllUserSerializer(Profile, many=True)
        response = {
            'data':serializer.data,
            'hasNext': len(serializer.data) == end - begin
        }
        return Response(response)

# class ResetPasswordView(APIView):