import uuid
from django.db import models
from django.conf import settings


class Interview(models.Model):
    INTERVIEW_TYPES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('mixed', 'Mixed'),
    ]
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviews')
    role = models.CharField(max_length=100)
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPES, default='mixed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_questions = models.IntegerField(default=5)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    technical_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    communication_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.role} - {self.status}"

    @property
    def answered_questions(self):
        from django.db.models import Count
        return self.questions.annotate(answer_count=Count('answers')).filter(answer_count__gt=0).count()

    @property
    def progress_percentage(self):
        if self.total_questions == 0:
            return 0
        return int((self.answered_questions / self.total_questions) * 100)


class Question(models.Model):
    QUESTION_TYPES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('situational', 'Situational'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='medium')
    order = models.IntegerField(default=0)
    expected_keywords = models.JSONField(default=list)
    time_limit_seconds = models.IntegerField(default=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order + 1}: {self.question_text[:50]}..."


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    audio_url = models.URLField(max_length=500, blank=True, null=True)
    is_voice_input = models.BooleanField(default=False)
    technical_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    communication_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)
    missing_points = models.JSONField(default=list, blank=True)
    keywords_found = models.JSONField(default=list, blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)
    evaluation_completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['answered_at']

    def __str__(self):
        return f"Answer to {self.question.id} by {self.user.email}"
