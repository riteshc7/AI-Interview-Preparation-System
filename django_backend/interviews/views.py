import httpx
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from .models import Interview, Question, Answer
from .forms import InterviewStartForm


def get_ai_service_url(path):
    return f"{settings.FASTAPI_URL}{path}"


@login_required
def start_interview(request):
    if request.method == 'POST':
        form = InterviewStartForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            interview_type = form.cleaned_data['interview_type']
            total_questions = form.cleaned_data['total_questions']
            
            interview = Interview.objects.create(
                user=request.user,
                role=role,
                interview_type=interview_type,
                total_questions=total_questions
            )
            
            try:
                with httpx.Client(timeout=60.0) as client:
                    response = client.post(
                        get_ai_service_url('/ai/generate-questions/'),
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
                    else:
                        messages.warning(request, 'Using default questions. AI service may be unavailable.')
                        create_default_questions(interview, total_questions)
            except Exception as e:
                messages.warning(request, f'AI service unavailable: {str(e)}. Using default questions.')
                create_default_questions(interview, total_questions)
            
            return redirect('interview_session', interview_id=interview.id)
    else:
        form = InterviewStartForm()
    
    return render(request, 'interview/start.html', {'form': form})


def create_default_questions(interview, total_questions):
    default_questions = {
        'backend developer': [
            {'question': 'Explain the difference between SQL and NoSQL databases.', 'type': 'technical', 'difficulty': 'easy', 'keywords': ['sql', 'nosql', 'relational', 'schema', 'scalability']},
            {'question': 'What is REST API and what are its principles?', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['rest', 'api', 'http', 'stateless', 'resources']},
            {'question': 'Describe how you would optimize a slow database query.', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['index', 'query', 'explain', 'join', 'cache']},
            {'question': 'What are microservices and when would you use them?', 'type': 'technical', 'difficulty': 'hard', 'keywords': ['microservices', 'monolith', 'api', 'deployment', 'scaling']},
            {'question': 'Explain the concept of ACID in databases.', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['atomicity', 'consistency', 'isolation', 'durability', 'transaction']},
        ],
        'frontend developer': [
            {'question': 'What is the difference between let, const, and var in JavaScript?', 'type': 'technical', 'difficulty': 'easy', 'keywords': ['var', 'let', 'const', 'scope', 'hoisting']},
            {'question': 'Explain the React component lifecycle.', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['mounting', 'updating', 'unmounting', 'useeffect', 'state']},
            {'question': 'How does the virtual DOM work in React?', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['virtual', 'dom', 'reconciliation', 'diffing', 'performance']},
            {'question': 'What are closures in JavaScript and when would you use them?', 'type': 'technical', 'difficulty': 'hard', 'keywords': ['closure', 'scope', 'function', 'lexical', 'encapsulation']},
            {'question': 'Describe the difference between CSS Grid and Flexbox.', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['grid', 'flexbox', 'layout', 'one-dimensional', 'two-dimensional']},
        ],
        'data scientist': [
            {'question': 'What is the difference between supervised and unsupervised learning?', 'type': 'technical', 'difficulty': 'easy', 'keywords': ['supervised', 'unsupervised', 'labeled', 'unlabeled', 'regression']},
            {'question': 'Explain the bias-variance tradeoff.', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['bias', 'variance', 'overfitting', 'underfitting', 'model complexity']},
            {'question': 'How would you handle missing data in a dataset?', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['imputation', 'deletion', 'interpolation', 'mean', 'median']},
            {'question': 'What is cross-validation and why is it important?', 'type': 'technical', 'difficulty': 'medium', 'keywords': ['cross-validation', 'k-fold', 'training', 'validation', 'generalization']},
            {'question': 'Explain the difference between L1 and L2 regularization.', 'type': 'technical', 'difficulty': 'hard', 'keywords': ['l1', 'l2', 'regularization', 'lasso', 'ridge', 'penalty']},
        ],
    }
    
    questions = default_questions.get(interview.role.lower(), default_questions['backend developer'])
    for idx in range(min(total_questions, len(questions))):
        q = questions[idx]
        Question.objects.create(
            interview=interview,
            question_text=q['question'],
            question_type=q['type'],
            difficulty=q['difficulty'],
            order=idx,
            expected_keywords=q['keywords'],
            time_limit_seconds=300
        )


@login_required
def interview_session(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    
    if interview.status == 'completed':
        return redirect('interview_results', interview_id=interview.id)
    
    questions = interview.questions.all()
    current_question = None
    next_question = None
    
    answered_ids = Answer.objects.filter(question__interview=interview).values_list('question_id', flat=True)
    
    for idx, q in enumerate(questions):
        if q.id not in answered_ids:
            current_question = q
            if idx + 1 < len(questions):
                next_question = questions[idx + 1]
            break
    
    if current_question is None:
        return redirect('interview_results', interview_id=interview.id)
    
    context = {
        'interview': interview,
        'question': current_question,
        'next_question': next_question,
        'progress': interview.progress_percentage,
        'total': interview.total_questions,
        'answered': interview.answered_questions,
    }
    return render(request, 'interview/session.html', context)


@login_required
def submit_answer(request, interview_id):
    if request.method == 'POST':
        interview = get_object_or_404(Interview, id=interview_id, user=request.user)
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer_text', '').strip()
        
        question = get_object_or_404(Question, id=question_id, interview=interview)
        
        if not answer_text:
            return JsonResponse({'success': False, 'error': 'Answer cannot be empty'}, status=400)
        
        answer = Answer.objects.create(
            question=question,
            user=request.user,
            answer_text=answer_text,
            is_voice_input=request.POST.get('is_voice') == 'true'
        )
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    get_ai_service_url('/ai/evaluate-answer/'),
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
                    answer.evaluation_completed_at = timezone.now()
                    answer.save()
                else:
                    answer.feedback = 'Evaluation service temporarily unavailable.'
                    answer.save()
        except Exception as e:
            answer.feedback = f'Evaluation error: {str(e)}'
            answer.save()
        
        return JsonResponse({
            'success': True,
            'feedback': answer.feedback,
            'technical_score': float(answer.technical_score) if answer.technical_score else 0,
            'communication_score': float(answer.communication_score) if answer.communication_score else 0,
            'missing_points': answer.missing_points
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def complete_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    
    if request.method == 'POST':
        from django.db.models import Avg
        
        interview.status = 'completed'
        interview.completed_at = timezone.now()
        
        answers = Answer.objects.filter(question__interview=interview)
        if answers.exists():
            tech_scores = [float(a.technical_score) for a in answers if a.technical_score]
            comm_scores = [float(a.communication_score) for a in answers if a.communication_score]
            
            interview.technical_score = round(sum(tech_scores) / len(tech_scores), 2) if tech_scores else 0
            interview.communication_score = round(sum(comm_scores) / len(comm_scores), 2) if comm_scores else 0
            interview.overall_score = round((interview.technical_score + interview.communication_score) / 2, 2)
        
        if interview.started_at:
            duration = timezone.now() - interview.started_at
            interview.duration_minutes = max(1, int(duration.total_seconds() / 60))
        
        interview.save()
        
        return redirect('interview_results', interview_id=interview.id)
    
    return redirect('interview_results', interview_id=interview.id)


@login_required
def interview_results(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id, user=request.user)
    questions = interview.questions.all()
    answers = Answer.objects.filter(question__interview=interview)
    
    answer_map = {str(a.question.id): a for a in answers}
    
    context = {
        'interview': interview,
        'questions': questions,
        'answers': answers,
        'answer_map': answer_map,
    }
    return render(request, 'interview/results.html', context)


@login_required
def interview_list(request):
    interviews = Interview.objects.filter(user=request.user)
    return render(request, 'interview/list.html', {'interviews': interviews})


def api_start_interview(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        interview = Interview.objects.create(
            user=request.user,
            role=data.get('role'),
            interview_type=data.get('interview_type', 'mixed'),
            total_questions=data.get('total_questions', 5)
        )
        
        return JsonResponse({'success': True, 'interview_id': str(interview.id)}, status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_submit_answer(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        interview_id = data.get('interview_id')
        question_id = data.get('question_id')
        answer_text = data.get('answer_text', '')
        
        interview = get_object_or_404(Interview, id=interview_id, user=request.user)
        question = get_object_or_404(Question, id=question_id, interview=interview)
        
        answer = Answer.objects.create(
            question=question,
            user=request.user,
            answer_text=answer_text
        )
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    get_ai_service_url('/ai/evaluate-answer/'),
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
                    answer.evaluation_completed_at = timezone.now()
                    answer.save()
        except:
            pass
        
        return JsonResponse({
            'success': True,
            'answer_id': str(answer.id),
            'technical_score': float(answer.technical_score) if answer.technical_score else 0,
            'communication_score': float(answer.communication_score) if answer.communication_score else 0
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)
