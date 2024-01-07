from django.urls import path
from .views import analyze_image, image_detail, add_comment, image_list

urlpatterns = [
    path('images/', image_list, name='image_list'),
    path('image/<int:id>/', image_detail, name='image_detail'),
    path('analyze-image/', analyze_image, name='analyze_image'),
    path('image/<int:id>/comment/', add_comment, name='add_comment')
]