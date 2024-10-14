from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.


# @api_view(['GET'])
# def hello_world(request):
#     print(request.body)
#     return Response({'msg':'Hello world!'})


# @api_view()
# def hello_world(request):
#     print(request.body)
#     return Response({'msg':'Hello world!'})

# @api_view(['POST'])
# def hello_world(request):
#     if request.method=="POST":
#         print(request.data)
#         return Response({'msg':'This is Post Request'})

@api_view(['GET','POST'])
def hello_world(request):
    if request.method=="GET":
        print(request.data)
        return Response({'msg':'This is Get Request'})
    if request.method=="POST":
        print(request.data)
        return Response({'msg':'This is Post Request',"data":request.data})
