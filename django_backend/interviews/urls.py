from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_interview, name='start_interview'),
    path('<uuid:interview_id>/', views.interview_session, name='interview_session'),
    path('<uuid:interview_id>/submit/', views.submit_answer, name='submit_answer'),
    path('<uuid:interview_id>/complete/', views.complete_interview, name='complete_interview'),
    path('<uuid:interview_id>/results/', views.interview_results, name='interview_results'),
    path('list/', views.interview_list, name='interview_list'),
    path('api/start/', views.api_start_interview, name='api_start_interview'),
    path('api/submit/', views.api_submit_answer, name='api_submit_answer'),
]
