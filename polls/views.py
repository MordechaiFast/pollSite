from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader
from .models import Question

def index(request):
    return render(request,'index.html',
     {'latest_question_list': Question.objects.order_by('-pub_date')[:5]})

def detail(request, question_id):
    try:
        return render(request, 'detail.html',
         {'question': Question.objects.get(pk=question_id)})
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

def results(request, question_id):
    return HttpResponse(f"The results of question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Voting on question {question_id}")