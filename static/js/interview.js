class InterviewSession {
    constructor(interviewId) {
        this.interviewId = interviewId;
        this.currentQuestion = null;
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
    }
    
    async submitAnswer(questionId, answerText) {
        const formData = new FormData();
        formData.append('question_id', questionId);
        formData.append('answer_text', answerText);
        formData.append('csrfmiddlewaretoken', this.getCSRFToken());
        
        try {
            const response = await fetch(`/interviews/${this.interviewId}/submit/`, {
                method: 'POST',
                body: formData
            });
            
            return await response.json();
        } catch (error) {
            console.error('Submit error:', error);
            throw error;
        }
    }
    
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    async toggleVoiceInput() {
        if (!this.isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);
                this.audioChunks = [];
                
                this.mediaRecorder.ondataavailable = (e) => {
                    this.audioChunks.push(e.data);
                };
                
                this.mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                    stream.getTracks().forEach(track => track.stop());
                };
                
                this.mediaRecorder.start();
                this.isRecording = true;
                this.updateVoiceButton(true);
            } catch (error) {
                console.error('Microphone access error:', error);
                alert('Could not access microphone. Please check permissions.');
            }
        } else {
            if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
                this.mediaRecorder.stop();
            }
            this.isRecording = false;
            this.updateVoiceButton(false);
        }
    }
    
    updateVoiceButton(recording) {
        const btn = document.getElementById('voiceBtn');
        const text = document.getElementById('voiceBtnText');
        
        if (recording) {
            btn.classList.add('text-red-500');
            text.textContent = 'Recording... Click to stop';
        } else {
            btn.classList.remove('text-red-500');
            text.textContent = 'Use Voice Input';
        }
    }
    
    displayFeedback(data) {
        const container = document.getElementById('feedbackContainer');
        if (!container) return;
        
        document.getElementById('techScore').textContent = `${data.technical_score.toFixed(1)}%`;
        document.getElementById('commScore').textContent = `${data.communication_score.toFixed(1)}%`;
        document.getElementById('feedbackText').textContent = data.feedback || 'No feedback available.';
        
        const missingList = document.getElementById('missingPointsList');
        missingList.innerHTML = '';
        if (data.missing_points && data.missing_points.length > 0) {
            data.missing_points.forEach(point => {
                const li = document.createElement('li');
                li.textContent = point;
                missingList.appendChild(li);
            });
        } else {
            document.getElementById('missingPointsContainer').style.display = 'none';
        }
        
        container.classList.remove('hidden');
        container.scrollIntoView({ behavior: 'smooth' });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const answerForm = document.getElementById('answerForm');
    if (answerForm) {
        const interviewMatch = window.location.pathname.match(/\/interviews\/([^\/]+)\//);
        if (interviewMatch) {
            const session = new InterviewSession(interviewMatch[1]);
            
            answerForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const submitBtn = this.querySelector('button[type="submit"]');
                const questionId = this.querySelector('input[name="question_id"]').value;
                const answerText = this.querySelector('textarea[name="answer_text"]').value;
                
                if (!answerText.trim()) {
                    alert('Please enter your answer.');
                    return;
                }
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Evaluating...';
                
                try {
                    const result = await session.submitAnswer(questionId, answerText);
                    
                    if (result.success) {
                        session.displayFeedback(result);
                        submitBtn.textContent = 'Submitted';
                        submitBtn.classList.remove('bg-primary');
                        submitBtn.classList.add('bg-green-600');
                    } else {
                        alert(result.error || 'Failed to submit answer');
                        submitBtn.disabled = false;
                        submitBtn.textContent = 'Submit Answer';
                    }
                } catch (error) {
                    alert('An error occurred. Please try again.');
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit Answer';
                }
            });
            
            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.addEventListener('click', () => session.toggleVoiceInput());
            }
        }
    }
});
