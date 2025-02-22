# from django.shortcuts import render

# from api.models import Profile, User,Todos
# from api.serializer import RegisterSerializer, MyTokenObtainPairSerializer,TodoSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework import generics, status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
#     serializer_class = RegisterSerializer

# class TodosListView(generics.ListCreateAPIView):
#     serializer_class = TodoSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
        
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             raise NotFound(detail=f"User with id {user_id} not found.")
        
#         # Get the todos associated with the user
#         todos = Todos.objects.filter(user=user)
#         return todos

# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TodoSerializer

#     def get_object(self):
#         user_id = self.kwargs.get('user_id')
#         todo_id = self.kwargs.get('id')

#         # Fetch the user, or raise a 404 if not found
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             raise NotFound(f"User with id {user_id} does not exist.")

#         # Fetch the todo, ensuring it's associated with the correct user
#         try:
#             todo = Todos.objects.get(id=todo_id, user=user)
#         except Todos.DoesNotExist:
#             raise NotFound(f"Todo with id {todo_id} does not exist for user {user_id}.")

#         return todo

# class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView): 
#     serializer_class = TodoSerializer

#     def get_object(self):
#         user_id = self.kwargs.get('user_id')
#         todo_id = self.kwargs.get('todo_id')

#          # Fetch the user, or raise a 404 if not found
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             raise NotFound(f"User with id {user_id} does not exist.")

#         # Fetch the todo, ensuring it's associated with the correct user
#         try:
#             todo = Todos.objects.get(id=todo_id, user=user)
#         except Todos.DoesNotExist:
#             raise NotFound(f"Todo with id {todo_id} does not exist for user {user_id}.")
        
#         Todos.completed = True
#         Todos.save()
        

        
        





# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def dashboard(request):
#     if request.method == "GET":
#         response = f"Hey {request.user}, you are seeing a GET response"
#         return Response({'response': response}, status=status.HTTP_200_OK)
#     else:
#         response = f"Hey {request.user}, you're using a POST response"
#         return Response({'response': response}, status=status.HTTP_200_OK)
#     return Response({}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from django.http import JsonResponse
from api.models import Profile, User,Todos,chatMessage

from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer, TodoSerializer,chatMessageSerializer,ProfileSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Subquery,OuterRef,Q


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Get All Routes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


class TodoListView(generics.ListCreateAPIView):
    queryset = Todos.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        todo = Todos.objects.filter(user=user) 
        return todo
    

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todos.objects.get(id=todo_id, user=user)

        return todo
    

class TodoMarkAsCompleted(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs['user_id']
        todo_id = self.kwargs['todo_id']

        user = User.objects.get(id=user_id)
        todo = Todos.objects.get(id=todo_id, user=user)

        todo.completed = True
        todo.save()

        return todo 
        

class MyInbox(generics.ListAPIView):
    serializer_class = chatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')


        messages = chatMessage.objects.filter(
            id__in=Subquery(
                User.objects.filter(
                    Q(sender__reciever = user_id)|
                    Q(reciever__sender = user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        chatMessage.objects.filter(
                            Q(sender = OuterRef('id'),reciever = user_id)|
                            Q(reciever = OuterRef('id'),sender = user_id)
                        ).order_by("-id")[:1].values_list("id",flat=True)
                    )
                ).values_list("last_msg",flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages 

class GetMessages(generics.ListAPIView):
    serializer_class =chatMessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages =  chatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id])
        return messages  


class SendMessages(generics.CreateAPIView):
    serializer_class = chatMessageSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self,request,*args,**kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = Profile.objects.filter(
            Q(user__username__icontains = username) |
            Q(full_name__icontains = username) |
            Q(user__email__icontains = username)
           

        ) 

        if not users.exists():
            return Response(
                {"detail":"No users founds"},
                status = status.HTTP_404_NOT_FOUND
            ) 
        else:
            serializer = self.get_serializer(users,many = True)
            return Response(serializer.data)




