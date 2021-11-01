from django.shortcuts import render
from opencv_webapp.forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

#주석

def simple_upload(request):
    if request.method == 'POST':#포스트 요청인지
        #유저로부터 제출된 요청이 post라면
        # print(request.POST) : <QueryDict: {'csrfmiddlewaretoken': [‘~~~’], 'title': ['upload_1']}>
        # print(request.FILES) : <MultiValueDict: {'image': [<InMemoryUploadedFile: ses.jpg (image/jpeg)>]}>
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = SimpleUploadForm(request.POST, request.FILES) #유저가 전송할 요청내용 꺼냄 / 업로
        #  request.FILES : 업로드한 파일만 따로 요청
        #request.POST : 파일제외한 모든요


        if form.is_valid():#함수실행결과가 true라면!문제가 없다고 판단된다면
            myfile = request.FILES['image'] # 'ses.jpg' #업로드한 파일 원본이 나옴 #업로드한 파일 변수에 저장
            fs = FileSystemStorage()# 클래스이름이야...
            filename = fs.save(myfile.name, myfile) #myfile.name,: 유저가 업로드한 파일 자체이름 # 경로명을 포함한 파일명 & 파일 객체
            # myfile.name : 'ses.jpg'
            # filename : 'ses. Udehdo.jpg'
            # 업로드된 이미지 파일의 URL을 얻어내 Template에게 전달
            uploaded_file_url = fs.url(filename) #저장마치면 유알엘도 돌려달라 # '/media/ses.jpg'
            #이자리에서 얼굴위치판단하는 프레딕트가 들어가기도함


            context = {'form': form, 'uploaded_file_url': uploaded_file_url}#바깥으로 내보내주는 역할  # filled form
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else: # request.method == 'GET' (DjangoBasic 실습과 유사한 방식입니다.)
        form = SimpleUploadForm()#빈양식
        context = {'form': form} # empty form
        return render(request, 'opencv_webapp/simple_upload.html', context)



def detect_face(request):
    if request.method == 'POST' :
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES)
        #request.POST : 포스트 통째로 넘겨주면되 굳이 ['']이렇게 지칭하지 않아도 됨
        #채워진 양식 만드는거야 (언제나 form을 쓴다고보면 됨) # filled form
        if form.is_valid():
            # 파일이 이미지 파일인지 / 유효한지 확인해줌
            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경하거나 추가로 다른 데이터를 추가할 수 있음
            post = form.save(commit=False)
            #임시저장하려는거야 post변수에 담아서 저장하는거
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장
	    # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (record 1건에 해당)

        # 저장이 끝난파일의 경로명을 받아낼 수 있음
            imageURL = settings.MEDIA_URL + form.instance.document.name
            #==form.instance.document.url
            #== post.document.urls
            #==/media/images/2021/10/29/ses_BSD.jpg

            #뒤에 네임을 적나 안적나 보기에는 똑같은데 네임없으면 파일객체로 보여지는거고 / NAME까지 넣으면 문자열 형태여서 다름
            #경로명 /media/ 까지 붙여주려면 위처럼 할 수 있는데 위에서 name이 아니라 url로 넣엊면
            # settings.MEDIA_URL  : /media/
            #form.instance : 채워진 양식하나
            #form.instance.document : 채워진 양식의 도큐먼트
	    # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정
            #따로 리턴받지않고 진행함 . 보통 다른때에서 변수넣고 키값으로 전달하며 진행할 수 있는데 아쉽
            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)

    else:#get요청시.
         form = ImageUploadForm() # empty form
         context = {'form':form}
         return render(request, 'opencv_webapp/detect_face.html', context)
