from django.db import models

# Create your models here.
class ImageUploadModel(models.Model): # Model 상속받음
#클래스 만들때 굳이 함수 넣을필요는 없어 views.py에서 다 가
    # blank=True : Form에서 빈 채로 저장되는 것을 허용 (views.py에서 활용한 .is_valid() 함수가 검증 진행 시)
    description = models.CharField(max_length=255, blank=True)
    # blank=True): 유저가 빈문자열 적어도 통과
    # upload_to : 저장될 파일의 경로를 지정 (ex. ‘images/2020/02/21/test_image.jpg’)
    document = models.ImageField(upload_to='images/%Y/%m/%d')
    # upload_to='images/%Y/%m/%d' : 자동으로 경로 잡아주도
    # images/%Y/%m/%d/~~~ .jpg이런식으로 저장될 것임( python strftime 참고해서 하면됨)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add : 자동으로 저장되는 시점을 기준으로 현재 시간을 세팅
