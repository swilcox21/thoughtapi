from django.db import models
from django.conf import settings

# Create your models here.
class Reminder(models.Model):
    owner = models.ForeignKey('auth.User', related_name='reminders', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    recurring = models.BooleanField(default=False)
    text = models.CharField(max_length=5000)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.text
