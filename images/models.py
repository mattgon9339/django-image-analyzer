from django.db import models

class AnalyzedImage(models.Model):
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    image = models.ForeignKey(AnalyzedImage, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)