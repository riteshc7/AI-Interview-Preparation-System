from django.urls import path
from . import views

urlpatterns = [
    path('auth/profile/', views.UserProfileView.as_view(), name='api_user_profile'),
    path('interviews/', views.InterviewListCreateView.as_view(), name='api_interviews'),
    path('interviews/<uuid:interview_id>/', views.InterviewDetailView.as_view(), name='api_interview_detail'),
    path('interviews/<uuid:interview_id>/questions/', views.QuestionListView.as_view(), name='api_questions'),
    path('interviews/<uuid:interview_id>/submit-answer/', views.AnswerSubmitView.as_view(), name='api_submit_answer'),
    path('analytics/summary/', views.AnalyticsSummaryView.as_view(), name='api_analytics_summary'),
]
