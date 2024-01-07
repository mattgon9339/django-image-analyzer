from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('', serve, {'document_root': settings.REACT_APP_DIR, 'path': 'index.html'}, name='react-app'),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.REACT_APP_DIR, 'path': 'index.html'}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^(?P<path>.*)$', serve, {'document_root': settings.REACT_APP_DIR}),
]