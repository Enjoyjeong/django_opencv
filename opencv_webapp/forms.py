from django import forms
from .models import ImageUploadModel

class SimpleUploadForm(forms.Form):#모델을 기반으로 만들어진것이 아니라 modelform이아니라 그냥 form
    title = forms.CharField(max_length=50)
# ImageField Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.
# file = forms.FileField(): 이미지가 아닌 어떤 파일이든 가능
    image = forms.ImageField()#이미지파일 업로드 간으#파일필드가 갖고있는 속성도 다 갖고있고 업로드 객체가 이미지 파일이 맞는지도 검ㄱ증함

    #models.py에서 부르던 Field형식그대로 따라감

class ImageUploadForm(forms.ModelForm):
# Form을 통해 받아들여야 할 데이터가 명시되어 있는 메타 데이터 (DB 테이블을 연결)
    class Meta:
        model = ImageUploadModel
        #moels.py의 실제 테이블 이름 적어준거야
        # Form을 통해 사용자로부터 입력 받으려는 Model Class의 field 리스트
        fields = ('description', 'document', ) # uploaded_at
        #유저로부터 form을 통해 받아들일 부분
        #문자열로 적어줘야함
