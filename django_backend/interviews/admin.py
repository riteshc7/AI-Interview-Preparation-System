from django.contrib import admin
from .models import Interview, Question, Answer


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'interview_type', 'status', 'overall_score', 'started_at']
    list_filter = ['status', 'interview_type', 'role']
    search_fields = ['user__email', 'role']
    readonly_fields = ['overall_score', 'technical_score', 'communication_score']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['interview', 'question_type', 'difficulty', 'order']
    list_filter = ['question_type', 'difficulty']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'technical_score', 'communication_score', 'answered_at']
    list_filter = ['is_voice_input']
    readonly_fields = ['technical_score', 'communication_score', 'feedback', 'keywords_found']
