from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class MergeRequest(models.Model):
    title = models.CharField(max_length=100)
    repo = models.CharField(max_length=100, default='')
    source_branch = models.CharField(max_length=100, default='')
    target_branch = models.CharField(max_length=100, default='')
    target_email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100, default='Open')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_opened = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('merge-request-detail', kwargs={'pk': self.pk})

