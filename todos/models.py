from django.db import models
from django.urls import reverse
from account.models import Account
from django.utils.html import format_html


class Todos (models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    createdate = models.DateTimeField(auto_now=True)
    Functor = models.ForeignKey(to=Account,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    done = models.BooleanField(default=False)
    descend = models.TextField(null=True)
    attachment = models.FileField(
        null=True,
        blank=True,
        upload_to='attachment/')
    donedate = models.DateTimeField(null=True)

    class Meta:
        ordering = ['title']



