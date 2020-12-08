from Post.models import Post
from Account.models import Renter
from Review.models import Review
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# class CreateReportView(APIView):
#     class CreateReportSerializer(serializers.ModelSerializer):
