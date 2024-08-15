import json
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from .forms import  LoginForm, SignupForm
from .models import UserDetails
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .Serializers import UserSerializer


def print(request):
    return HttpResponse("Hello, world!")

def signup(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            signupForm.save()
            messages.success(
                request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        signupForm = SignupForm()
    return render(request, 'Loginify/signup.html', {'signupForm': signupForm})



def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            email = loginForm.cleaned_data.get('Email')
            password = loginForm.cleaned_data.get('Password')
            
            try:
                userDetails = UserDetails.objects.get(
                    Email=email, Password=password)
                request.session['user'] = email      
                return redirect('login_success')
            except UserDetails.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        loginForm = LoginForm()
    return render(request, 'Loginify/login.html', {'loginForm': loginForm})


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
        
    if request.method == 'POST':
        input_data = json.loads(request.body)
        serialized_data = UserSerializer(data=input_data)

        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse(serialized_data.data, status=201)
        else:
            return JsonResponse(serialized_data.errors, status=400)
    

@csrf_exempt
def single_user_data(request,email):
    if request.method =='GET':
        try:
            user_data=UserDetails.objects.get(Email=email)
            serialized_data = UserSerializer(user_data)
            return JsonResponse(serialized_data.data,safe=False)
        
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=500) 
        
    if request.method == 'PUT':
        try:
            user_data = UserDetails.objects.get(Email=email)
            input_data = json.loads(request.body)
            serialized_data = UserSerializer(user_data, data=input_data)

            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse(serialized_data.data, status=200)
        except:
            return JsonResponse({"error": "Failed to update data"}, status=500)
    
        

    if request.method == 'PATCH':
            try:
                user_data = UserDetails.objects.get(Email=email)
                input_data = json.loads(request.body)
                serialized_data = UserSerializer(user_data, data=input_data, partial=True)

                if serialized_data.is_valid():
                    serialized_data.save()
                    return JsonResponse(serialized_data.data, status=200)
                else:
                    return JsonResponse(serialized_data.errors, status=400)
            except UserDetails.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)


    if request.method == 'DELETE':
        try:
            user = UserDetails.objects.get(Email=email)
            user.delete()
            return JsonResponse({"success": "User deleted successfully"}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=400)

