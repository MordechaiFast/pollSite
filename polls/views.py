from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):
        """Returns the 5 most recently published questions"""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form with error message
        return render(request, 'detail.html',
         {'question': question,
          'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
         args=(question_id,) ))