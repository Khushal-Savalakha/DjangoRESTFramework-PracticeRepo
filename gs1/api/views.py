from django.shortcuts import render
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse,JsonResponse
# Model Object -Single Student Data
def Student_detail(request,pk):
    stu=Student.objects.get(id=pk)
    # print('1]',stu)
    serializer=StudentSerializer(stu)#dict data
    # print('2',serialzer)
    # print('3',serialzer.data)
    # json_data=JSONRenderer().render(serialzer.data)
    # return HttpResponse(json_data,content_type='application/json')
    return JsonResponse(serializer.data)

#Query Set-All Student Data
def Student_list(request):
    stu=Student.objects.all()
    # print('1]',stu)
    serializer=StudentSerializer(stu,many=True)#non dict data (dict data in form of list like [{},{}]
    # print('2',serialzer)
    # print('3',serialzer.data)
    # json_data=JSONRenderer().render(serialzer.data)
    # return HttpResponse(json_data,content_type='application/json')
    return JsonResponse(serializer.data,safe=False)