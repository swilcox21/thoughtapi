from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
# from api.permissions import IsOwnerOrReadOnly
from api.models import Reminder
from api.serializers import UserSerializer, ReminderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class ReminderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, reminder_id=None):
        print('request.data', self)
        if reminder_id is not None:
            reminder = get_object_or_404(Reminder.objects.all(), id = reminder_id)
            serialized_reminder = ReminderSerializer(reminder)
            return Response(serialized_reminder.data)
        all_reminders = Reminder.objects.filter(owner=request.user.id)
        serializer = ReminderSerializer(all_reminders, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ReminderSerializer(data=request.data)
        print('user', request.user)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,reminder_id):
        reminder = get_object_or_404(Reminder.objects.all(), id=reminder_id)
        ser_reminder = ReminderSerializer(instance=reminder, data=request.data, partial=True)
        if ser_reminder.is_valid(raise_exception=True):
            ser_reminder.save()
        return Response(ser_reminder.data, status=204)
    def delete(self,request,reminder_id):
        reminder = get_object_or_404(Reminder.objects.all(), id=reminder_id)
        reminder.delete()
        return Response({"message": "data: `{}` has been deleted".format(reminder_id)},status=204)


