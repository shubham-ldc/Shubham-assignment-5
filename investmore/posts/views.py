from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PostSerializer
from uuid import uuid4 as v4
from ..utils.helpers import  write_data_to_json_file,update_json_file,get_user_details,read_data_from_json_file



class CreatePostApiView(APIView):
    def post(self,request):
        try:
            post_data = request.data
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
            post_data['created_by'] = request.GET['id']
            serializer = PostSerializer(data = post_data)
            
            if serializer.is_valid():
                post_data = serializer.data
                post_data['_id'] = str(v4())
                # print(post_data)
                write_data_to_json_file(post_data,'posts.json')

                update_json_file(post_data['created_by'] ,{"created_post":post_data["_id"]},'users.json')


                return Response({"data": post_data, "message": "post created successfully"}, 201)

            return Response(serializer.errors, 400)
        except Exception as error:
            print(error)
            return Response('Internal server Error', 500)
        

class GetAllPostApiView(APIView):
    def get(self,request):
        all_post_data = read_data_from_json_file('posts.json')
        return Response({
            "data":all_post_data,
            "message":"All Scheme data retrive successfully"
        },200)