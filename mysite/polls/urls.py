from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    # the 'name' value as called by the {% url %}
    # added the word 'specifics'
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
    #path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
