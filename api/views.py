from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser,UserThread

class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self,request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class SpecificUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def get(self,request):
        if request.user.is_authenticated:
            current_user = request.user
            print(current_user.username)
            user_data = {
                'username':request.user.username,
            }
            return JsonResponse ({'user':user_data},status=200)
        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)


class CreatePost(APIView):
    permission_classes = (permissions.AllowAny,)

    def post (self,request):
        data = request.data
        serializer = CreatePostSerializer(data = data)
        if serializer.is_valid():
            authordata = request.user.username
            print(authordata)
            serializer.save()
            return Response({**serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CreateComment(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        data = request.data
        
        serializer = CreateCommentonPost(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({**serializer.data},status=status.HTTP_200_OK)
        else:
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

class GetCommentThreads(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,request,pk):
        post_id = UserThread.objects.get(id = pk)
        getthreadscomments = Comment.objects.filter(user_thread = post_id)
        serializer = GetCommentsonPostSerializer(getthreadscomments,many = True)
        return Response(serializer.data)
    

class PostGet(APIView):
    permission_classes =(permissions.AllowAny,)
    def get(self,request):
        posts = UserThread.objects.all()
        serializer = GetPostSerializer(posts, many = True)
        return Response(serializer.data)
    
class GetMembers(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self,request):
        members = Members.objects.all()
        serializer = GetMembersSerializer(members, many = True)
        return Response(serializer.data)
    
class PostMember(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        data = request.data
        serializer = GetMembersSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class PostGetUser(APIView):
    permission_classes= (permissions.AllowAny,)
    def get(self,request,pk):
        userid = CustomUser.objects.get(id = pk)
        userposts = UserThread.objects.filter(author = userid)
        serializer = GetUserPostSerializer(userposts, many = True)
        return Response(serializer.data)



class UpdateUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def put(self, request, pk):
        data = request.data
        userid = CustomUser.objects.get(id = pk)
        serializer = UpdateUserSerializer(instance= userid, data=data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeletePost(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def delete(self, request, pk):
        try: 
            postid = UserThread.objects.get(id = pk)
            postid.delete()
            return Response({"message : Post deleted Successfully"}, status=status.HTTP_200_OK)
        except UserThread.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


class UpdatePost(APIView):
    permission_classes = (permissions.AllowAny,)
    def put(self, request, pk):
        data=request.data
        postid = UserThread.objects.get(id = pk)
        serializer = UpdatePostSerializer(instance=postid,data=data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SearchUser(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self, request):
        query = request.query_params.get('query')
        if query:
            results = CustomUser.objects.filter(username__icontains=query)
            serializer = SearchUserSerializer(results, many=True)
            results_data = serializer.data
        else:
            results_data =[]
        return Response(results_data)
    
