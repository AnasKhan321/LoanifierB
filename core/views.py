from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Loan
import jwt
import json
from datetime import date
from rest_framework.decorators import api_view
from .Serilizaer import LoanSerializer
from rest_framework.response import Response

# Create your views here.

# Headers and Secrets form Encode Token Available for Global
header = {
    "alg": "HS256",
    "typ": "JWT"
}

secret = "bedardaya"

# Testing Function
def index(request):
    return HttpResponse('this is here ')


@csrf_exempt
# HandleSignup  Function Where user Signup
def handleSignup(request):
    try:
        if request.method == 'POST':
            bytes_data = request.body

            # Convert bytes to string
            string_data = bytes_data.decode('utf-8')
            json_data = json.loads(string_data)
            firstName = json_data.get('fname')
            lastName = json_data.get('lname')
            email = json_data.get('email')
            pass1 = json_data.get('pass1')
            username = json_data.get('username')

            print(username, firstName, lastName, email, pass1)

            if len(pass1) < 8:
                return JsonResponse({"error": "Password is To Short   "})

            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.save()
            payload = {
                "id": myuser.id
            }
            # Encode the Token to Send auth Token
            encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)
            return JsonResponse({"auth": encoded_jwt, "user": myuser.username})
    except Exception as j:
        return JsonResponse({'error': 'this s erro '})

# handle Login Function
@csrf_exempt
def handleLogin(request):
    print(request)
    try:
        if request.method == 'POST':
            bytes_data = request.body
            string_data = bytes_data.decode('utf-8')  # Use the appropriate encoding
            json_data = json.loads(string_data)  #Loads the data user send through Frontend

            # Get the Data
            username = json_data.get('loginusername')
            password = json_data.get('loginpass')

            user1 = authenticate(username=username, password=password)

            if user1 is not None:
                payload = {
                    "id": user1.id
                }
                # Encode the Token to Send auth Token
                encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)

                return JsonResponse({"auth": encoded_jwt, "user": username, 'detail': 'save'})

            else:
                return JsonResponse({"error": "SignUp First"})

        else:

            return JsonResponse({"error": "SignUp First"})
    except Exception as j:
        return JsonResponse({'error': j})


# Register Loan for User
@csrf_exempt
def handleLoan(request):
    if request.method == 'POST':
        bytes_data = request.body


        string_data = bytes_data.decode('utf-8')  # Use the appropriate encoding

        json_data = json.loads(string_data)
        print(json_data)
        vs = json_data.get('auth')
        decoded_jwt = jwt.decode(vs, secret, algorithms=['HS256'])
        user = User.objects.get(id=decoded_jwt.get('id'))
        amount = json_data.get('amount')
        repayment = json_data.get('timee')
        installment = json_data.get('installment')
        DAte = date.today()

        if Loan.objects.filter(user=user).exists():
            return JsonResponse({'request' : "Pay your First loan "})

        else:
            requestl = Loan(user=user,amount=amount,term=repayment,installment=installment,date=DAte)
            requestl.save()

            return  JsonResponse({'request' : 'saved'})


# Fetch the User specific Loan
@api_view(('GET',))
def getLoan(request):

    decoded_jwt = jwt.decode(request.headers.get('Auth'), secret, algorithms=['HS256'])
    user = User.objects.get(id=decoded_jwt.get('id'))
    loans = Loan.objects.filter(user=user)

    # Serilizing the Data to Send to User With the Help of Rest API
    serializer = LoanSerializer(loans, many=True)
    print(serializer.data)
    return Response(serializer.data)
