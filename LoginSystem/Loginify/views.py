import json
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignUpForm, LoginForm
from .models import UserDetails
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

from .Serializers import UserSerializer


def print(request):
    return HttpResponse("Hello, world!")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Account created successfully!')
            return redirect('login')  
    else:
        form = SignUpForm()
    return render(request, 'Loginify/signup.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('Password')
            
            try:
                user = UserDetails.objects.get(Username=username)
                if check_password(password, user.Password):
                    request.session['user'] = username
                    return redirect('login_success')
                else:
                    messages.error(request, 'Invalid username or password.')
            except UserDetails.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'Loginify/login.html', {'form': form})


def login_success(request):
    username = request.session.get('user', 'Guest')
    return render(request, 'Loginify/login_success.html', {'username': username})



def all_user_data(request):
    if request.method =='GET':
        try:
            user_data = UserDetails.objects.all()
            serialized_data = UserSerializer(user_data,many=True)
            return JsonResponse(serialized_data.data,safe=False)
        except:
            return JsonResponse({"error":"Failed to fetch data"},status=500) 
    

@csrf_exempt
def single_user_data(request,pk):
    if request.method =='GET':
        try:
            user_data=UserDetails.objects.get(pk=pk)
            serialized_data = UserSerializer(user_data)
            return JsonResponse(serialized_data.data,safe=False)
        
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404) 
    
        

    if request.method == 'PATCH':
            try:
                user_data = UserDetails.objects.get(Username=pk)
                input_data = json.loads(request.body)
                serialized_data = UserSerializer(user_data, data=input_data, partial=True)

                if serialized_data.is_valid():
                    serialized_data.save()
                    return JsonResponse(serialized_data.data, status=200)
                else:
                    return JsonResponse(serialized_data.errors, status=400)
            except UserDetails.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def delete_user_by_email(request, email):
    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(Email=email)
            user.delete()
            return JsonResponse({"success": "User deleted successfully"}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)

