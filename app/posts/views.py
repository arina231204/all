import telebot
from django.conf import settings
from rest_framework import viewsets, response, status, generics
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response

from posts.models import Posts, Comments, Rating
from posts.permissions import OwnerPermission
from posts.serializers import PostsSerializer, CommentsSerializer, RatingSerializer
from rest_framework.decorators import permission_classes


bot = telebot.TeleBot("5486116860:AAFrxHGH-14Kb59eLhb1sKEYZkyr1vo5pb0", parse_mode=None)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [OwnerPermission]
    authentication_classes = [TokenAuthentication, BasicAuthentication]


    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user.author)
        bot.send_message(post.author.telegram_chat_id, "Your post has been successfully published!")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Post successfully published."}, status=status.HTTP_201_CREATED, headers=headers)




class CommentsList(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [AllowAny]



class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

