from django.urls import path
from . import views # 같은 폴더 내의 views.py를 import
from django.conf import settings
from django.conf.urls.static import static
#유저가 파일 업로드할경우 위의 import라인 거의 그대로 받아서감

app_name = 'opencv_webapp'

urlpatterns = [
    path('', views.first_view, name='first_view'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),
    path('detect_face/', views.detect_face, name='detect_face'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static(settings: 이렇게 땡겨옴 / url처리를 해줌
#MEDIA_URL : 변수를 땡겨오는 방법
# static(settings.MEDIA_URL : static('media/')
# MEDIA_URL = '/media/'
#그냥 미디어폴더만 이렇게 해주는거야 다른폴더면 이렇게 안하긴해
