from django.conf import settings
import numpy as np
import cv2 #opencv_python

def cv_detect_face(path): # path parameter를 통해 파일 경로를 받아들이게 됩니다.
    img = cv2.imread(path, 1)
                # cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)
                #./media/images/2021/10/29/ses_BSD.jpg => path
                #imread : 이미지 로드된거 받아들이는것임
    if (type(img) is np.ndarray):
        print(img.shape) # 세로, 가로, 채널(405, 598, 3)

        resize_needed = False
        #이미지가 640,480보다 작으면 리사이즈 안함 / 사이즈 큰거면 true로 바꿔줄거여서 리사이즈됨
        if img.shape[1] > 640: # ex) 가로(img.shape[1])가 1280일 경우,
            resize_needed = True
            new_w = img.shape[1] * (640.0 / img.shape[1]) # 1280 * (640/1280) = 1280 * 0.5
            new_h = img.shape[0] * (640.0 / img.shape[1]) # 기존 세로 * (640/1280) = 기존 세로 * 0.5
        elif img.shape[0] > 480: # ex) 세로(img.shape[0])가 960일 경우,
            resize_needed = True
            new_w = img.shape[1] * (480.0 / img.shape[0]) # 기존 가로 * (480/960) = 기존 가로 * 0.5
            new_h = img.shape[0] * (480.0 / img.shape[0]) # 960 * (480/960) = 960 * 0.5

        if resize_needed == True:
            img = cv2.resize(img, (int(new_w), int(new_h)))#원본 덮어쓰기

        # Haar-based Cascade Classifier : AdaBoost 기반 머신러닝 물체 인식 모델
        # 이미지에서 눈, 얼굴 등의 부위를 찾는데 주로 이용
        # 이미 학습된 모델을 OpenCV 에서 제공 (http://j.mp/2qIxrxX)
        #저장된 파일 불러들이는 과정임
        # baseUrl = './media/'
        baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
        face_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_frontalface_default.xml')
        #정면대상으로 얼굴이 있는지 판별해줌
        eye_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_eye.xml')
        #눈의 위치찾음
        #CascadeClassifier : 이미지처리기법이야 / 사이즈가 다른 네모를 이미지 위에 얹어보면 비슷한 특징이 있는지 확인하는 모델
        #xml파일 media에 로딩 해놨음

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #원본이미지 주면서 컬러를 그레이로 해달라
        #컬러이미지 가져오게되면 rgb일텐데/ 흑백처리하면 처리하는 시간과 용량이 훨신 줄어듦(만들려는게 색이 의미가 없다면 흑백처리하는ㄴ게 더 좋아 성속도도 빠르고 용량도 적어)
# detectMultiScale(Original img, ScaleFactor, minNeighbor) : further info. @ http://j.mp/2SxjtKR
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #원본이미지 대상으로 얼굴찾아줌
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)#(x+w, y+h) : 너비, 높이
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray) #눈위치 뽑고
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)#위치별로 네모를 그리고
        cv2.imwrite(path, img)
        #얼굴마다 눈들을 네모로 그려줄거지

    else:
        print('Error occurred within cv_detect_face!')
        print(path)


# 파이썬파일 만들어놓고 함수로 넣어서 적용시키는거야
