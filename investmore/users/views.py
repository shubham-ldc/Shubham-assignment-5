from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSignupSerializer,UserLoginSerializer
from uuid import uuid4 as v4
from ..utils.helpers import  write_data_to_json_file, hash_user_password \
      ,validate_hash_password,get_user_details,get_user_scheme_data,get_user_post_data \
      , create_user_scheme_portfolio


class UserSignupApiView(APIView):
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data = request.data)
            
            if serializer.is_valid():
                user_data = serializer.data

                user_email = get_user_details("email",user_data['email'])

                if user_email:
                    return Response({
                        "data":None,
                        "message":"duplicate email error"
                    },400)

                # hash the user given password
                user_data['password'] = hash_user_password(user_data['password'])
                user_data['_id'] = str(v4())
                user_data['created_scheme'] = []
                user_data['created_post'] = []


                # write to json file
                write_data_to_json_file(user_data,'users.json')

                # remove password field before returning response 
                user_data.pop('password')

                return Response({"data": user_data, "message": "user created successfully"}, 201)

            return Response(serializer.errors, 400)
        except Exception as error:
            print(error)
            return Response('Internal server Error', 500)


class UserLoginApiView(APIView):
    def post(self, request):
        try:
            user_login_data = request.data
            # print("user_login_data", user_login_data)
            serializer_data = UserLoginSerializer(data=user_login_data)

            if not serializer_data.is_valid():
                return Response({
                    "data":None,
                    "message": "Please Provide detail in valid format."
                }, status=401)
            
            user_data = get_user_details("email",serializer_data.validated_data['email'])
            if not user_data:
                return Response({
                    "data": None,
                    "message": "Invalid username."
                },status=404)
            
            hash_password = validate_hash_password(serializer_data.validated_data['password'], user_data['password'])
            if not hash_password:
                return Response({
                    "data":None,
                    "message": "Invalid Credential"
                }, status=404)
            
            return Response({
                "data" : {},
                "message" : "Login Successfully"
            }, status=200)
        except Exception as e:
            print(e)
            return Response({
                "data": None,
                "message": f"Something went wrong. Please Try again.... {str(e)}"
            })
    
class GetUserschemeApiView(APIView):
    def get(self,request):
        try:
            if "id" not in request.GET:
                return Response({
                    "data":None,
                    "message":"user id required"
                },400)
            
            user = get_user_details("_id" , request.GET["id"])

            if not user:
                return Response({
                    "data":None,
                    "message":"invalid user id"
                },400)
            
            user_scheme_data = get_user_scheme_data(request.GET["id"])

            return Response({
                "data":user_scheme_data,
                "message":"user scheme retrive succesfully"
            },200)
        except Exception as e:
            print(e)
            return Response({
                "data": None,
                "message": f"Something went wrong. Please Try again.... {str(e)}"
            })
        
class GetUserPortfolio(APIView):
    def get(self,request):
        try:
            if "id" not in request.GET:
                return Response({
                    "data":None,
                    "message":"user id require"
                },400)
            
            user = get_user_details("_id" , request.GET["id"])

            if not user:
                return Response({
                    "data":None,
                    "message":"invalid user id"
                },400)
            
            user_portfolio = create_user_scheme_portfolio(request.GET["id"])
            print(user_portfolio)

            return Response({
                "data":user_portfolio,
                "message":"user portfolio retrive succesfully"
            },200)
        except Exception as e:
            print(e)
            return Response({
                "data": None,
                "message": f"Something went wrong. Please Try again.... {str(e)}"
            })
        
class GetUserpostApiView(APIView):
    def get(self,request):
        try:
            if "id" not in request.GET:
                return Response({
                    "data":None,
                    "message":"user id require"
                },400)
            
            user = get_user_details("_id" , request.GET["id"])

            if not user:
                return Response({
                    "data":None,
                    "message":"invalid user id"
                },400)
            
            user_post_data = get_user_post_data(request.GET["id"])

            return Response({
                "data":user_post_data,
                "message":"user post retrive succesfully"
            },200)
        except Exception as e:
            print(e)
            return Response({
                "data": None,
                "message": f"Something went wrong. Please Try again.... {str(e)}"
            })