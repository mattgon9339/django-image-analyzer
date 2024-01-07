from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import AnalyzedImage, Comment
from .serializers import AnalyzedImageSerializer, CommentSerializer
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageCommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        image = Image.new("RGB", (100, 100))
        image_file = io.BytesIO()
        image.save(image_file, "JPEG")
        image_file.seek(0)
        self.image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")

    def test_analyze_image_view(self):
        # URL for the analyze_image view
        url = reverse("analyze_image")

        # Prepare the request data with the image file
        data = {"file": self.image}

        # Send a POST request to the view
        response = self.client.post(url, data, format="multipart")

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the expected keys in the response data
        self.assertIn("image_id", response.data)
        self.assertIn("image", response.data)
        self.assertIn("description", response.data)

        # Assert that an AnalyzedImage object was created in the database
        self.assertTrue(AnalyzedImage.objects.filter(id=response.data["image_id"]).exists())

    def test_analyze_image(self):
        analyzed_image = AnalyzedImage.objects.create(description="Test Image")
        url = reverse('add_comment', kwargs={'id': analyzed_image.id})
        data = {'comment': 'Test Comment'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.last()
        self.assertEqual(comment.text, 'Test Comment')
        self.assertEqual(response.data['comment_id'], comment.id)
        self.assertEqual(response.data['msg'], 'Comment added successfully!')

    def test_add_comment(self):
        analyzed_image = AnalyzedImage.objects.create(description="Test Image")
        url = reverse('add_comment', kwargs={'id': analyzed_image.id})
        data = {'comment': 'Test Comment'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment = Comment.objects.last()
        self.assertEqual(comment.text, 'Test Comment')
        self.assertEqual(response.data['comment_id'], comment.id)
        self.assertEqual(response.data['msg'], 'Comment added successfully!')

    def test_image_list(self):
        AnalyzedImage.objects.create(description="Test Image 1")
        AnalyzedImage.objects.create(description="Test Image 2")

        url = reverse('image_list')
        last_image_id = 0

        # Set the HTTP header for the last image id
        self.client.defaults['HTTP_LAST_IMAGE_ID'] = last_image_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        images = AnalyzedImage.objects.filter(id__gt=last_image_id)[:5]
        serializer = AnalyzedImageSerializer(images, many=True)
        self.assertEqual(response.data['images'], serializer.data)

    def test_image_detail(self):
        analyzed_image = AnalyzedImage.objects.create(description="Test Image")
        Comment.objects.create(image=analyzed_image, text="Test Comment 1")
        Comment.objects.create(image=analyzed_image, text="Test Comment 2")

        url = reverse('image_detail', kwargs={'id': analyzed_image.id})
        last_comment_id = 0

        # Set the HTTP header for the last comment id
        self.client.defaults['HTTP_LAST_COMMENT_ID'] = last_comment_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comments = Comment.objects.filter(image_id=analyzed_image.id, id__gt=last_comment_id)[:10]
        comment_serializer = CommentSerializer(comments, many=True)
        serializer = AnalyzedImageSerializer(analyzed_image)
        self.assertEqual(response.data['image'], serializer.data)
        self.assertEqual(response.data['comments'], comment_serializer.data)