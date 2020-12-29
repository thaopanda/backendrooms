from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from Chat.models import Thread, ChatMessage
from Account.models import Host

class GetThread(APIView):
    class ThreadSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = '__all__'

    def get(self, request, format=None):
        thread = Thread.objects.by_user(user=request.user)
        serializer = self.ThreadSerializer(thread, many=True)
        return Response(serializer.data)

class GetChat(APIView):
    class ChatSerializer(serializers.ModelSerializer):
        class Meta:
            model = ChatMessage
            fields = ['message']

    def get(self, request, pk,begin, end, format=None):
        thread = Thread.objects.get(pk=pk)
        chat = ChatMessage.objects.filter(thread=thread).order_by('timestamp')[begin:end]
        serializer = self.ChatSerializer(chat, many=True)
        response = {
            'data':serializer.data,
            'hasNext': len(serializer.data) == end - begin
        }
        return Response(response)

class GetThreadAdmin(APIView):
    class ThreadSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = '__all__'

    def get(self, request, username, format=None):
        user = Host.objects.get(username=username)
        thread = Thread.objects.by_user(user=user)
        serializer = self.ThreadSerializer(thread, many=True)
        return Response(serializer.data)