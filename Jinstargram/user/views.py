import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from Jinstargram.settings import MEDIA_ROOT

# Create your views here.

class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        #TODO 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email = email, nickname = nickname,
                            name = name, password = make_password(password),
                            profile_image = "default_profile.jpg")

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

class LogOut(APIView):
    def get(self, request):
        #flush을 통해 세션을 날려줌
        request.session.flush()
        return render(request, 'user/login.html')


class UploadProfile(APIView):
    def post(self, request):
        file = request.FILES['file']
        email = request.data.get('email')

        # 파일의 이름을 정하기 위한 것
        uuid_name = uuid4().hex  # 랜덤으로 고유의 값을 가지도록 도와줌
        save_path = os.path.join(MEDIA_ROOT, uuid_name)  # 프로젝트 위치(mediaroot)/media/uuid4(ehkfdl과 같은 랜덤)

        # 파일을 open해서 저장하는 부분
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email= email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)  # 200은 http의 성공코드