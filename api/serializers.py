from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
import random
from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
UserModel = get_user_model()


class CustomUserSerializer(UserSerializer):
    
    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = ("customuser_id", 'profilepic')

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['uid'] = instance.id
    #     data['profile_picture'] = instance.profile_picture.url if instance.profile_picture else None
    #     return data
    
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields = ('id','email','username','password')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields=('email','username','profilepic')

class CustomUserWithVerificationSerializer(CustomUserSerializer):
    is_verified = serializers.BooleanField()  # Assuming is_verified is a field in your UserModel

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'is_verified')

class Verification(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields=('email','is_verified')

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    OTP = serializers.CharField(max_length = 6)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username','profilepic',)

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserThread
        fields = ('author','title', 'caption','image',)

    def create(self, validated_data,):
        create_post = UserThread.objects.create(
             author = validated_data['author'],
             title=validated_data['title'],
             caption=validated_data['caption'],
             image = validated_data.pop('image',None))
        
        return create_post
    
class CreateCommentonPost(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user_thread', 'author','text',)
    def create(self, validated_data):
        create_comment = Comment.objects.create(
            user_thread = validated_data['user_thread'],
            author = validated_data['author'],
            text = validated_data['text'])
        
        return create_comment
    

class GetCommentsonPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source = 'author.username', read_only=True)
    author_profile = serializers.CharField(source = 'author.profilepic',read_only=True)
    class Meta:
        model = Comment
        fields = ['author','author_username','author_profile','user_thread','text','created_at']

class GetUserPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source = 'author.username', read_only=True)
    author_profile = serializers.CharField(source = 'author.profilepic',read_only=True)
    class Meta:
        model = UserThread
        fields = ['id','author','author_username','author_profile','title','caption','image','created_at']

        
class GetPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source = 'author.username', read_only=True)
    author_profile = serializers.CharField(source = 'author.profilepic',read_only=True)
    class Meta:
        model = UserThread
        fields = ['id','author','author_username','author_profile', 'title','caption','image','created_at']

class GetMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class PostMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ('first_name','last_name','age',)


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserThread
        fields = ('caption',)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email','profilepic')

# class PostSerializer(serializers.ModelSerializer):
#     thread_title
        

# {
#     "email": "lname@gmail.com",
#     "password": "halo123123"
# }
