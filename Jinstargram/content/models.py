from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField() #글내용
    image = models.TextField()  #피드 이미지
    email = models.EmailField(default='') #글쓴이

class Like(models.Model):
    feed_id = models.IntegerField(default=0) #어떤 글을 좋아요 눌렀는지
    email = models.EmailField(default='')  # 좋아요 누른 사람
    is_like = models.BooleanField(default=True) #좋아요를 누를수도 있고 취소할수도 있음(업데이트 하기위해)

class Reply(models.Model):
    feed_id = models.IntegerField(default=0)  # 어떤 글에 댓글을 달았는지
    email = models.EmailField(default='')  # 댓글 단 사람
    reply_content = models.TextField()

class BookMark(models.Model):
    feed_id = models.IntegerField(default=0)  # 어떤 글을 북마크 했는지
    email = models.EmailField(default='')  # 북마크 한 사람
    is_marked = models.BooleanField(default=True)