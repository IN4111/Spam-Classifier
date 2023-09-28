from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import AllRecords

from src.SpamClassifier import SpamClassifierModel

Model=SpamClassifierModel()

class Home(TemplateView):
    template_name="index.html"
class Author(TemplateView):
    template_name="author.html"
def Records(request):
    data=[]
    for record in AllRecords.objects.all().order_by("-createdAt"):
        dict={}
        dict["message"]=record.message
        dict["spam"]=record.spam
        dict["createdAt"]=record.createdAt.strftime("%d/%m/%Y %H:%M")
        data.append(dict)
    return render(request,"record.html",context={"records":data})
def Result(request):
    data=request.GET.get("text",None)
    if(data!=None):
        result=Model.predict(data)[0]
        if(result):
            spam=True
        else:
            spam=False
        AllRecords.objects.create(message=data,spam=spam)
        return render(request,"result.html",context={"result":spam})
    else:
        return HttpResponse("Requested Get is not acceptable")
