from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from interviews.models import Interview, Answer
from django.utils import timezone
from datetime import timedelta


@login_required
def performance_view(request):
    interviews = Interview.objects.filter(user=request.user, status='completed')
    
    total_interviews = interviews.count()
    avg_score = interviews.aggregate(Avg('overall_score'))['overall_score__avg'] or 0
    avg_technical = interviews.aggregate(Avg('technical_score'))['technical_score__avg'] or 0
    avg_communication = interviews.aggregate(Avg('communication_score'))['communication_score__avg'] or 0
    
    recent_interviews = interviews[:5]
    
    score_history = list(interviews.order_by('completed_at').values(
        'completed_at', 'overall_score', 'technical_score', 'communication_score'
    ))
    
    role_stats = interviews.values('role').annotate(
        count=Count('id'),
        avg_score=Avg('overall_score')
    ).order_by('-count')
    
    context = {
        'total_interviews': total_interviews,
        'avg_score': round(avg_score, 1),
        'avg_technical': round(avg_technical, 1),
        'avg_communication': round(avg_communication, 1),
        'recent_interviews': recent_interviews,
        'score_history': score_history,
        'role_stats': list(role_stats),
    }
    
    return render(request, 'analytics/performance.html', context)


@login_required
def api_analytics_summary(request):
    interviews = Interview.objects.filter(user=request.user, status='completed')
    
    data = {
        'total_interviews': interviews.count(),
        'avg_overall_score': round(float(interviews.aggregate(Avg('overall_score'))['overall_score__avg'] or 0), 1),
        'avg_technical_score': round(float(interviews.aggregate(Avg('technical_score'))['technical_score__avg'] or 0), 1),
        'avg_communication_score': round(float(interviews.aggregate(Avg('communication_score'))['communication_score__avg'] or 0), 1),
        'total_questions_answered': Answer.objects.filter(user=request.user).count(),
    }
    
    return JsonResponse(data)


@login_required
def api_analytics_performance(request):
    interviews = Interview.objects.filter(user=request.user, status='completed')
    
    last_30_days = timezone.now() - timedelta(days=30)
    recent = interviews.filter(completed_at__gte=last_30_days)
    
    score_history = []
    for interview in interviews.order_by('completed_at'):
        score_history.append({
            'date': interview.completed_at.isoformat() if interview.completed_at else None,
            'score': float(interview.overall_score) if interview.overall_score else 0,
            'role': interview.role
        })
    
    return JsonResponse({'score_history': score_history})


@login_required
def api_analytics_role(request):
    interviews = Interview.objects.filter(user=request.user, status='completed')
    
    role_data = interviews.values('role').annotate(
        count=Count('id'),
        avg_score=Avg('overall_score'),
        avg_technical=Avg('technical_score'),
        avg_communication=Avg('communication_score')
    ).order_by('-count')
    
    return JsonResponse({'roles': list(role_data)})
