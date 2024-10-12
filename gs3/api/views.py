# from django.shortcuts import render
# import io
# from .models import Student
# from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
# from django.http import HttpResponse
# from .serializers import StudentSerializer
# # Create your views here.
# def student_api(request):
#     if request.method =='GET':
#         json_data=request.body
#         stream=io.ByteIo(json_data)
#         pythondata=JSONparser().parse(stream)
#         #it converts binary form data into python dictionary
#         # (python native data)
#         id=pythondata.get('id',None)
#         if id is not None:
#             stu=Student.objects.get(id=id)
#             serializer=StudentSerializer(stu)
#             json_data=JSONRenderer().render(serializer.data)
#             return HttpResponse(json_data,content_type='application/json')

from django.shortcuts import render
import io
from api.models import Student
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse
from .serializers import StudentSerializer
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        # Get the raw JSON data from the request body
        json_data = request.body

        # Convert the JSON data (in bytes) into a stream of bytes
        stream = io.BytesIO(json_data)
        print('stream:',stream)
        # Parse the byte stream to convert it into a Python dictionary
        pythondata = JSONParser().parse(stream)

        # Extract the 'id' from the parsed data, if available
        id = pythondata.get('id', None)

        if id is not None:
            # Fetch the student object based on the provided 'id'
            stu = Student.objects.get(id=id)

            # Serialize the student object into a JSON-compatible format
            serializer = StudentSerializer(stu)

            # Render the serialized data as JSON
            json_data = JSONRenderer().render(serializer.data)

            # Return the JSON data as an HTTP response
            return HttpResponse(json_data, content_type='application/json')
        else:
            stu=Student.objects.all()
            serializer=StudentSerializer(stu,many=True)
            # Render the serialized data as JSON
            json_data = JSONRenderer().render(serializer.data)
            # Return the JSON data as an HTTP response
            return HttpResponse(json_data,content_type='application/json')    
    if request.method=='POST':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        serializer=StudentSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data Created'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        else:
            json_data=JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')
    if request.method=='PUT':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id=pythondata.get('id')
        stu=Student.objects.get(id=id)
        #Complete Update - Required All Data from Front End/Client
        #serializer = StudentSerializer(stu, data=pythondata)
        #Partial Update - All Data not required
        serializer=StudentSerializer(stu,data=pythondata,partial=True)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data Updated'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        else:
            json_data=JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')
    if request.method=='DELETE':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id=pythondata.get('id')
        stu=Student.objects.get(id=id)
        stu.delete()
        res={'msg':'Data Deleted!!'}
        # json_data=JSONRenderer().render(res)
        # return HttpResponse(json_data,content_type='application/json')
        return JsonResponse(res,safe=False)
