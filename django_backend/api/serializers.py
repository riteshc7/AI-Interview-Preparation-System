from rest_framework import serializers
from users.models import CustomUser
from interviews.models import Interview, Question, Answer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone', 'target_role', 'experience_level']
        read_only_fields = ['id', 'email']


class InterviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'role', 'interview_type', 'status', 'overall_score', 'started_at', 'completed_at']


class InterviewDetailSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    answered_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Interview
        fields = [
            'id', 'role', 'interview_type', 'status', 'overall_score',
            'technical_score', 'communication_score', 'started_at',
            'completed_at', 'total_questions', 'duration_minutes',
            'questions_count', 'answered_count'
        ]
    
    def get_questions_count(self, obj):
        return obj.questions.count()
    
    def get_answered_count(self):
        return self.instance.answers.count() if hasattr(self, 'instance') else 0


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'difficulty', 'order', 'time_limit_seconds']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id', 'question', 'answer_text', 'is_voice_input',
            'technical_score', 'communication_score', 'feedback',
            'missing_points', 'keywords_found', 'answered_at'
        ]
        read_only_fields = ['technical_score', 'communication_score', 'feedback', 'missing_points', 'keywords_found']


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    answer_text = serializers.CharField(min_length=10)
    is_voice_input = serializers.BooleanField(default=False)
