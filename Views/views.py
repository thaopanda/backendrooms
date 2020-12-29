from Post.models import Post
from Account.models import Renter
from Views.models import Views
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator
from datetime import datetime, timedelta, timezone, tzinfo

class ViewsOnPost(APIView):
    def get(self,request, pk, format=None):
        post = Post.objects.get(pk=pk)
        result = []
        for i in range(7):
            time = datetime.now().date()-timedelta(days=i)
            count = Views.objects.filter(post=post, time=time).count()
            obj = (time, count)
            result.append(obj)
        response = {
            'views':result
        }
        return Response(response)
