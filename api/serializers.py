from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    text = serializers.CharField(required=False, allow_blank=True, max_length=5000)
    class Meta:
        model = Reminder
        fields = ['id','owner','created','recurring','text']
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.recurring = validated_data.get('recurring', instance.recurring)
        instance.save()
        return instance
    def create(self, validated_data):
        return Reminder.objects.create(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    # reminders = serializers.PrimaryKeyRelatedField(many=True, queryset=Reminder.objects.all())
    reminders = ReminderSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'reminders']