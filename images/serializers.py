from rest_framework import serializers
from .models import AnalyzedImage, Comment

class AnalyzedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedImage
        fields = ['id', 'image', 'description', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']
