import httpx
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from interviews.models import Interview, Question, Answer


class UserProfileView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'is_authenticated': True,
                'id': str(request.user.id),
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'full_name': request.user.get_full_name(),
                'experience_level': request.user.experience_level,
                'target_role': request.user.target_role,
            })
        return Response({'is_authenticated': False})


class InterviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        interviews = Interview.objects.filter(user=request.user)
        data = [{
            'id': str(i.id),
            'role': i.role,
            'interview_type': i.interview_type,
            'status': i.status,
            'overall_score': float(i.overall_score) if i.overall_score else None,
            'started_at': i.started_at.isoformat(),
            'completed_at': i.completed_at.isoformat() if i.completed_at else None,
        } for i in interviews]
        return Response(data)
    
    def post(self, request):
        role = request.data.get('role')
        interview_type = request.data.get('interview_type', 'mixed')
        total_questions = request.data.get('total_questions', 5)
        
        interview = Interview.objects.create(
            user=request.user,
            role=role,
            interview_type=interview_type,
            total_questions=total_questions
        )
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{settings.FASTAPI_URL}/ai/generate-questions/",
                    json={
                        'role': role,
                        'interview_type': interview_type,
                        'total_questions': total_questions,
                        'experience_level': request.user.experience_level or 'mid'
                    }
                )
                if response.status_code == 200:
                    questions_data = response.json()['questions']
                    for idx, q_data in enumerate(questions_data):
                        Question.objects.create(
                            interview=interview,
                            question_text=q_data['question'],
                            question_type=q_data.get('type', 'technical'),
                            difficulty=q_data.get('difficulty', 'medium'),
                            order=idx,
                            expected_keywords=q_data.get('keywords', []),
                            time_limit_seconds=q_data.get('time_limit', 300)
                        )
        except Exception:
            pass
        
        return Response({'id': str(interview.id)}, status=201)


class InterviewDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, interview_id):
        try:
            interview = Interview.objects.get(id=interview_id, user=request.user)
        except Interview.DoesNotExist:
            return Response({'error': 'Interview not found'}, status=404)
        
        data = {
            'id': str(interview.id),
            'role': interview.role,
            'interview_type': interview.interview_type,
            'status': interview.status,
            'overall_score': float(interview.overall_score) if interview.overall_score else None,
            'technical_score': float(interview.technical_score) if interview.technical_score else None,
            'communication_score': float(interview.communication_score) if interview.communication_score else None,
            'started_at': interview.started_at.isoformat(),
            'completed_at': interview.completed_at.isoformat() if interview.completed_at else None,
            'total_questions': interview.total_questions,
            'answered_questions': interview.answered_questions,
            'progress_percentage': interview.progress_percentage,
        }
        return Response(data)


class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, interview_id):
        try:
            interview = Interview.objects.get(id=interview_id, user=request.user)
        except Interview.DoesNotExist:
            return Response({'error': 'Interview not found'}, status=404)
        
        questions = interview.questions.all()
        data = [{
            'id': str(q.id),
            'question_text': q.question_text,
            'question_type': q.question_type,
            'difficulty': q.difficulty,
            'order': q.order,
            'time_limit_seconds': q.time_limit_seconds,
        } for q in questions]
        return Response(data)


class AnswerSubmitView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, interview_id):
        try:
            interview = Interview.objects.get(id=interview_id, user=request.user)
        except Interview.DoesNotExist:
            return Response({'error': 'Interview not found'}, status=404)
        
        question_id = request.data.get('question_id')
        answer_text = request.data.get('answer_text', '')
        
        try:
            question = Question.objects.get(id=question_id, interview=interview)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=404)
        
        answer = Answer.objects.create(
            question=question,
            user=request.user,
            answer_text=answer_text
        )
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{settings.FASTAPI_URL}/ai/evaluate-answer/",
                    json={
                        'question': question.question_text,
                        'answer': answer_text,
                        'expected_keywords': question.expected_keywords,
                        'question_type': question.question_type
                    }
                )
                if response.status_code == 200:
                    eval_data = response.json()
                    answer.technical_score = eval_data.get('technical_score', 0)
                    answer.communication_score = eval_data.get('communication_score', 0)
                    answer.feedback = eval_data.get('feedback', '')
                    answer.missing_points = eval_data.get('missing_points', [])
                    answer.keywords_found = eval_data.get('keywords_found', [])
                    answer.save()
        except Exception:
            pass
        
        return Response({
            'id': str(answer.id),
            'technical_score': float(answer.technical_score) if answer.technical_score else 0,
            'communication_score': float(answer.communication_score) if answer.communication_score else 0,
            'feedback': answer.feedback,
            'missing_points': answer.missing_points,
        }, status=201)


class AnalyticsSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        interviews = Interview.objects.filter(user=request.user, status='completed')
        
        from django.db.models import Avg, Count
        
        data = {
            'total_interviews': interviews.count(),
            'avg_overall_score': round(float(interviews.aggregate(Avg('overall_score'))['overall_score__avg'] or 0), 1),
            'avg_technical_score': round(float(interviews.aggregate(Avg('technical_score'))['technical_score__avg'] or 0), 1),
            'avg_communication_score': round(float(interviews.aggregate(Avg('communication_score'))['communication_score__avg'] or 0), 1),
            'total_questions_answered': Answer.objects.filter(user=request.user).count(),
            'role_breakdown': list(
                interviews.values('role').annotate(
                    count=Count('id'),
                    avg_score=Avg('overall_score')
                ).order_by('-count')
            ),
        }
        return Response(data)
