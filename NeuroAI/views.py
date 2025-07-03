from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .models import RegisterUser, Questions, Response as ResponseTable , DisorderSave,Disorder,PasswordReset,ChatHistory
from .serializers import RegisterSerializer,LoginSerializer, QuestionsSerializer, ResponseSerializer,BulkResponseSerializer, DisorderSerializer, LogoutSerializer,ResetPasswordRequestSerializer,ResetPasswordSerializer,ChatHistorySerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response 
from rest_framework import status,permissions
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import json
from django.conf import settings

# Create your views here.

# class Chatbot(APIView):
    # def post(self, request):
    #     url = "https://openrouter.ai/api/v1/chat/completions"
    #     # token = "settings.OPENROUTER_API_KEY"
    #     # Prantik's API key
    #     token = "settings.OPENROUTER_API_KEY"

    #     data = {
    #         "model": "meta-llama/llama-3.3-8b-instruct:free",
    #         "messages": [
    #             {
    #                 "role": "user",
    #                 "content": "Hi!"  # Or get from request.data.get("user_input")
    #             }
    #         ]
    #     }

    #     json_data = json.dumps(data)
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {token}",
    #         "Content-Length": str(len(json_data))
    #     }

    #     try:
    #         response = requests.post(url, headers=headers, data=json_data)
    #         response.raise_for_status()
    #         return Response(response.json())  # Return API response to the user
    #     except requests.exceptions.RequestException as e:
    #         return Response({"error": str(e)}, status=500)



class Chatbot(APIView):
    def post(self, request):
        url = "https://openrouter.ai/api/v1/chat/completions"
        token = settings.OPENROUTER_API_KEY
        # print(f"OPENROUTER_API_KEY = {token}")
        user_input = request.data.get('user_input', '').strip()
        
        if not user_input:
            return Response({"error": "user_input is required"}, status=400)
        
        # if not user_input:
            # return Response({
            #     "id": "gen-1749393824-wCx5Tyly2cljW1rmG8bd",
            #     "choices": [{
            #         "message": {
            #             "role": "assistant",
            #             "content": "Hello! How can I assist you?"
            #         }
            #     }],
            # })
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            # "HTTP-Referer": "http://127.0.0.1:8000/",
            # "X-Title": "neuroAI"
        }
        
        payload = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [{"role": "user", "content": user_input}]
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return Response(response.json())
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response:
                error_msg = e.response.text
            return Response({"error": error_msg}, status=500)


# class RegisterView(generics.CreateAPIView):
#     queryset = RegisterUser.objects.all()
#     serializer_class = RegisterSerializer
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response ({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status= status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"message": "Invalid credentials"}, status=401)
        
class logoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request,*args, **kwargs):
        serializer =  self.serializer_class(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print('email', email)
            user = RegisterUser.objects.filter(email=email).first()
            print(user)

            if user:
               token_generator = PasswordResetTokenGenerator()
               token = token_generator.make_token(user)
               reset = PasswordReset(email=email, token=token)
               reset.save()
            #       Add your frontend url of forgot password
            #    reset_url = f'http://localhost:5173/password_reset/confirm/{token}'
            #    reset_url = f'http://192.168.0.102:5173/password_reset/confirm/{token}'
            #    reset_url = f'https://neuro-ai-client.vercel.app/password_reset/confirm/{token}'
               reset_url = f"""
                NeuroAI Client(old domain): https://neuro-ai-client.vercel.app/password_reset/confirm/{token}
                NeuroAICS(new domain): https://neuroaics.vercel.app/password_reset/confirm/{token}
                """
               print(reset_url)
               send_mail(
                   'Password Reset Request',
                   f'Please choose any one link that matches your preferred domain, to reset password: {reset_url}',
                   'prantik.ghosh59@gmail.com',
                   [email],
                   fail_silently=False
                   )
               return Response({"message": "Password reset link has been sent to your email"}, status=200)
            else:
               return Response({"message": "User not found"}, status=404)
        return Response(serializer.errors, status=400)
                
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['password']
        confirm_password = data['confirmpassword']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = RegisterUser.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)
                
class QuestionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args, **kwargs):
        questions = Questions.objects.all()
        question_list = [{"id":q.id,"question": q.question} for q in questions]
        question_res = {'questions': question_list}
        return Response(question_res)
    
# class ResponseView(viewsets.ModelViewSet):
#     serializer_class = ResponseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # def get_queryset(self):
#     #     return ResponseTable.objects.filter(user = self.request.user)
#     def perform_create(self, serializer):
#         print(serializer)
#         serializer.save(user=self.request.user)

class ResponseView(generics.GenericAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user= self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BulkResponseView(generics.GenericAPIView):
    serializer_class = BulkResponseSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            responses_data = serializer.save()
            responses_serialized_data = ResponseSerializer(responses_data, many=True).data
            return Response({"responses": responses_serialized_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])    
def Disorder_recommendation(request):
    if request.method == 'GET':
        user_responses = ResponseTable.objects.filter(user=request.user, response = "Yes")
        print(user_responses)
        count = user_responses.count()
        print(count)
        question_id = user_responses.values_list('question_id', flat = True)
        print(question_id)
        disorder_id = DisorderSave.objects.filter(question_id__in=question_id).values_list('disorder_id', flat=True)
        print(disorder_id)
        disorders = Disorder.objects.filter(id__in=disorder_id).distinct()
        print(disorders)
        disorder_serializer = DisorderSerializer(disorders, many=True)
        print(disorder_serializer)
        data = {
            "disorders": disorder_serializer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)
        
class ChatHistoryView(generics.GenericAPIView):
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        
        user = request.user
        new_data = request.data 
        if not isinstance(new_data, list):
            return Response({"error": "Invalid data format. Expected a list."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = ChatHistory.objects.get(user=user)
            try:
                existing_history = json.loads(chat.history)
            except json.JSONDecodeError:
                existing_history = []
            existing_history.extend(new_data)
            chat.history = json.dumps(existing_history)
        except ChatHistory.DoesNotExist:
            chat = ChatHistory(user=user, history=json.dumps(new_data))

        chat.save()
        return Response(new_data, status=status.HTTP_200_OK)
    
    def get (self,request, *args, **kwargs):
        user = request.user
        try:
            chat = ChatHistory.objects.get(user=user)
            return Response(json.loads(chat.history), status=status.HTTP_200_OK)
        except ChatHistory.DoesNotExist:
            return Response([], status=200)
        

            
            
        

        






        
    




       
        

            

            

        

        
            
        
    
    

        

        
        
    

    





    
        



    


    

    
        

        

    
       



        

