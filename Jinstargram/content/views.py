import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Jinstargram.settings import MEDIA_ROOT
from .models import Feed, Reply,Like,BookMark  # .models.는 나와 같은 폴더에 있는 파일들을 가르킴
from user.models import User

class Main(APIView):
    def get(self, request):

        email = request.session.get('email', None)


        if email is None:
            return render(request, 'user/login.html')

        # change user = User.objects.filter(email=email).first()
        main_user = User.objects.filter(email=email).first() #로그인한 메인 아이디 경진

        if main_user is None: # change user->main
            return render(request, 'user/login.html')

        feed_object_list = Feed.objects.all().order_by('-id')  # select * from content_feed;
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first() #미밍밍
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))


            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            is_marked = BookMark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()

            feed_list.append(dict(id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname,
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked
                                  ))

        return render(request, 'jinstargram/main.html', context=dict(feeds=feed_list,user=main_user))


class UploadFeed(APIView):
    def post(self, request):
        file = request.FILES['file']

        # 파일의 이름을 정하기 위한 것
        uuid_name = uuid4().hex  # 랜덤으로 고유의 값을 가지도록 도와줌
        save_path = os.path.join(MEDIA_ROOT, uuid_name)  # 프로젝트 위치(mediaroot)/media/uuid4(ehkfdl과 같은 랜덤)

        # 파일을 open해서 저장하는 부분
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        content = request.data.get('content')
        image = uuid_name
        email = request.session.get('email', None)

        Feed.objects.create(content=content, image=image, email=email)

        return Response(status=200)  # 200은 http의 성공코드

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'user/login.html')

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')

        feed_list = Feed.objects.filter(email=email).all()
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True)) #[게시물 아이디 출력]
        Like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(BookMark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        BookMark_feed_list = Feed.objects.filter(id__in=bookmark_list)

        return render(request, 'content/profile.html', context=dict(feed_list =feed_list, user=user,
                                                                    Like_feed_list=Like_feed_list,
                                                                    BookMark_feed_list=BookMark_feed_list))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id',None)
        reply_content = request.data.get('reply_content',None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)  # 200은 http의 성공코드

class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id',None)
        favorite_text = request.data.get('favorite_text',True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)  # 200은 http의 성공코드

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id',None)
        bookmark_text = request.data.get('bookmark_text',True)

        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = BookMark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            BookMark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)  # 200은 http의 성공코드