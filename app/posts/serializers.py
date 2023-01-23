from rest_framework import serializers

from posts.models import Posts, Comments, Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('author',)

class PostsSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ('id','text', 'create_at', 'average_rating', 'author')
        read_only_fields = ['author']

    def get_average_rating(self, obj):
        return obj.average_rating()




class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

