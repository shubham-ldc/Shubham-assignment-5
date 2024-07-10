from rest_framework.views import APIView
from .serializers import SchemeSerializer
from rest_framework.response import Response

from uuid import uuid4 as v4
from ..utils.helpers import  write_data_to_json_file, update_json_file,get_user_details \
    ,create_post_data,read_data_from_json_file , get_top_n_investment_schemes


class CreateSchemeApiView(APIView):

    def post(self,request):
        try:
            scheme_data = request.data
            print(request.GET['id'])
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
            scheme_data['created_by'] = request.GET['id']
            serializer = SchemeSerializer(data = scheme_data)
            
            if serializer.is_valid():
                scheme_data = serializer.data
                scheme_data['_id'] = str(v4())
                print(scheme_data)
                write_data_to_json_file(scheme_data, 'schemes.json')

                update_json_file(scheme_data['created_by'] ,{"created_scheme":scheme_data["_id"]},'users.json')

                if scheme_data.get('create_post') == True:
                    post_data = create_post_data(scheme_data)
                    print(post_data)
                    update_json_file(scheme_data['created_by'] , {
                        'created_post': post_data['_id']
                    }, 'users.json')
                    write_data_to_json_file(post_data, 'posts.json')

                

                return Response({"data": scheme_data, "message": "scheme created successfully"}, 201)

            return Response(serializer.errors, 400)
        except Exception as error:
            print(error)
            return Response('Internal server Error', 500)

class GetAllSchemeApiView(APIView):
    def get(self,request):
        try:
            all_schemes_data = read_data_from_json_file('schemes.json')
            return Response({
                "data":all_schemes_data,
                "message":"All Scheme data retrive successfully"
            },200)
        except Exception as error:
            print(error)
            return Response('Internal server Error', 500)
    

class GetTopSchemeApiView(APIView):
    def get(self,request):
        try:
            top_n = int(request.GET['n'])
            print(top_n)
            top_n_inestment_scheme = get_top_n_investment_schemes(top_n) 
            print("hello",top_n_inestment_scheme)
            return Response({
                "data":top_n_inestment_scheme,
                "message":f"top {top_n} scheme retrive successfully"
            },200)
        except Exception as error:
            print(error)
            return Response('Internal server Error', 500)
