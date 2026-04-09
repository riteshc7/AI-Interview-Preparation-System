from django.urls import path
from . import views

urlpatterns = [
    path('', views.performance_view, name='performance'),
    path('api/summary/', views.api_analytics_summary, name='api_analytics_summary'),
    path('api/performance/', views.api_analytics_performance, name='api_analytics_performance'),
    path('api/role-analysis/', views.api_analytics_role, name='api_analytics_role'),
]
