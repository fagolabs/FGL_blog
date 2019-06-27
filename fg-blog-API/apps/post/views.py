# users/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from apps.authen import models as auth_models, serializers as auth_serializers


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all().order_by('-create_time')
    serializer_class = serializers.PostSerializer


class AuthorOfPostView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        if post_id:
            try:
                post_data = models.Post.objects.get(id=int(post_id))
            except models.Post.DoesNotExist:
                post_data = None

            if post_data:
                author_id = post_data.author.id
                author_data = auth_models.CustomUser.objects.get(id=author_id)
                serial = auth_serializers.UserSerializer(author_data)
                return Response(serial.data)
            else:
                return Response({"error": "post id not exist!"})
        else:
            return Response({"error": "Post id is not provided"})


class PostClipViewSet(viewsets.ModelViewSet):
    queryset = models.PostClipsUser.objects.all()
    serializer_class = serializers.PostClipSerializer


class PostClipFindView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        post_id = kwargs.get('post_id', None)
        user_id = kwargs.get('user_id', None)
        if post_id and user_id:
            post_clip = models.PostClipsUser.objects.filter(post=post_id, user=user_id).first()

            if post_clip:
                return Response({'status': True, 'clip_id': post_clip.id})
            else:
                return Response({'status': False, 'clip_id': None})
