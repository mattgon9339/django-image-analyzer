from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from google.cloud import vision_v1
from .models import AnalyzedImage, Comment
from .serializers import AnalyzedImageSerializer, CommentSerializer


# View for adding an image and description
@api_view(['POST'])
def analyze_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        description = ''
        if image:
            analyzed_image = AnalyzedImage.objects.create(image=image, description=description)

            # Initialize the Vision API client
            client = vision_v1.ImageAnnotatorClient()

            # Specify the path to the image file you want to analyze
            image_path = str(settings.BASE_DIR) + analyzed_image.image.url

            # Read the image file and convert it to a bytes-like object
            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            # Create an Image object with the image content
            image = vision_v1.Image(content=content)

            # Specify the types of analysis you want to perform (e.g., LABEL_DETECTION, TEXT_DETECTION)
            # You can add additional features as needed
            features = [
                vision_v1.Feature(type=vision_v1.Feature.Type.LABEL_DETECTION),
                vision_v1.Feature(type=vision_v1.Feature.Type.TEXT_DETECTION),
            ]

            # Create a request object with the image and features
            request = vision_v1.AnnotateImageRequest(image=image, features=features)

            # Perform the image analysis
            response = client.annotate_image(request)

            # Extract information from the response
            labels = [label.description for label in response.label_annotations]
            description = ", ".join(labels)
            analyzed_image.description = description
            analyzed_image.save()

        return Response({'image_id': analyzed_image.id, 'image': analyzed_image.image.url, 'description': description})


# View for adding a comment to a specific analyzed image
@api_view(['POST'])
def add_comment(request, id):
    # Get the comment text from the request data
    comment_text = request.data.get('comment', None)

    # Retrieve the analyzed image based on the provided ID
    analyzed_image = AnalyzedImage.objects.filter(id=id).first()

    # Create a new comment associated with the analyzed image
    comment = Comment.objects.create(image=analyzed_image, text=comment_text)

    # Return a response with the ID of the added comment and a success message
    return Response({'comment_id': comment.id, 'msg': 'Comment added successfully!'})


# View for retrieving a list of analyzed images
@api_view(['GET'])
def image_list(request):
    # Retrieve the last image ID from the request headers
    last_image_id = request.META.get('HTTP_LAST_IMAGE_ID', None)

    # Query the database for images with IDs greater than the last ID
    images = AnalyzedImage.objects.filter(id__gt=last_image_id)[:5]

    # Serialize the images and return the response
    serializer = AnalyzedImageSerializer(images, many=True)
    return Response({'images': serializer.data})


# View for retrieving details of a specific analyzed image, including associated comments
@api_view(['GET'])
def image_detail(request, id):
    # Retrieve the image based on the provided ID
    image = get_object_or_404(AnalyzedImage, id=id)

    # If the request method is GET, retrieve the last comment ID from the request headers
    last_comment_id = request.META.get('HTTP_LAST_COMMENT_ID', None)

    # Query the database for comments associated with the image and with IDs greater than the last comment ID
    comments = Comment.objects.filter(image_id=id, id__gt=last_comment_id)[:10]

    # Serialize the image and associated comments, then return the response
    comment_serializer = CommentSerializer(comments, many=True)
    serializer = AnalyzedImageSerializer(image)
    return Response({'image': serializer.data, 'comments': comment_serializer.data})
