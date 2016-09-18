from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView
from django.utils import timezone


# def index(request):
#     last_question_list = Question.objects.order_by('-put_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'lastest_question_list': last_question_list
#     }
#     return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        return Question.objects.filter(put_date__lte=timezone.now()).order_by('-put_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request,'polls/detail.html',{'question':question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})
#
#
def vote(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question, 'error_message':'You must select one choice'})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args = (question.id,)))

