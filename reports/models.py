from django.db import models
from profiles.models import Profile
from django.urls import reverse

class Report(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    remark = models.TextField()
    image = models.ImageField(upload_to='reports/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('reports:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "Report for: " + self.author.user.username + ' --- ' + self.name

    class Meta:
        ordering = ['-created']