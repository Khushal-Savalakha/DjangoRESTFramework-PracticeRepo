from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def student_create(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=python_data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                res = {'msg': 'Data Created'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json')
            except Exception as e:
                # Log the exception for debugging purposes
                print(f"Exception occurred: {e}")
                res = {'errors': str(e)}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data, content_type='application/json', status=400)
        else:
            res = {'errors': serializer.errors}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json', status=400)
    return HttpResponse({'message': 'Method not allowed'}, status=405)
