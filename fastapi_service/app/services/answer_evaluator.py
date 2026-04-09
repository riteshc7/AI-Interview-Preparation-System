import re
from typing import List, Set
from ..models.schemas import EvaluateAnswerRequest, EvaluationResponse


class AnswerEvaluator:
    def __init__(self):
        self.communication_indicators = {
            "good": [
                "for example", "specifically", "in particular", "such as",
                "because", "therefore", "thus", "consequently",
                "first", "second", "finally", "additionally",
                "however", "although", "nevertheless", "meanwhile",
                "in conclusion", "to summarize", "in summary"
            ],
            "weak": [
                "um", "uh", "like", "you know", "basically",
                "stuff", "things", "some stuff", "whatever"
            ]
        }
        
        self.structure_indicators = [
            r"\d+\.", r"[a-z]\)", r"first|second|third|finally",
            r"on the other hand", r"in contrast", r"additionally",
            r"moreover", r"furthermore"
        ]
    
    def evaluate(self, request: EvaluateAnswerRequest) -> EvaluationResponse:
        answer_lower = request.answer.lower()
        
        keywords_found = self._find_keywords(request.expected_keywords, answer_lower)
        keyword_score = self._calculate_keyword_score(keywords_found, request.expected_keywords)
        
        technical_score = keyword_score * 0.7 + self._evaluate_depth(answer_lower, request.question_type) * 0.3
        
        communication_score = self._evaluate_communication(request.answer)
        
        feedback = self._generate_feedback(keywords_found, request.expected_keywords, communication_score)
        missing_points = self._get_missing_points(keywords_found, request.expected_keywords)
        
        return EvaluationResponse(
            technical_score=round(technical_score, 1),
            communication_score=round(communication_score, 1),
            feedback=feedback,
            missing_points=missing_points,
            keywords_found=keywords_found
        )
    
    def _find_keywords(self, expected: List[str], answer: str) -> List[str]:
        found = []
        for keyword in expected:
            keyword_lower = keyword.lower()
            if keyword_lower in answer:
                found.append(keyword)
            else:
                for word in keyword_lower.split():
                    if len(word) > 3 and word in answer:
                        found.append(keyword)
                        break
        return found
    
    def _calculate_keyword_score(self, found: List[str], expected: List[str]) -> float:
        if not expected:
            return 75.0
        return min((len(found) / len(expected)) * 100, 100)
    
    def _evaluate_depth(self, answer: str, question_type: str) -> float:
        min_length = 50
        ideal_length = 300
        
        if len(answer) < min_length:
            return 40.0
        
        depth_score = min((len(answer) / ideal_length) * 100, 100)
        
        example_patterns = [r"for example", r"such as", r"like", r"instance"]
        if any(re.search(p, answer) for p in example_patterns):
            depth_score += 10
        
        detail_words = [r"\d+%?", r"\d+ times", r"specific", r"detailed"]
        if any(re.search(p, answer) for p in detail_words):
            depth_score += 5
        
        return min(depth_score, 100)
    
    def _evaluate_communication(self, answer: str) -> float:
        answer_lower = answer.lower()
        
        good_count = sum(1 for phrase in self.communication_indicators["good"] if phrase in answer_lower)
        weak_count = sum(1 for phrase in self.communication_indicators["weak"] if phrase in answer_lower)
        
        structure_score = 50
        for pattern in self.structure_indicators:
            if re.search(pattern, answer, re.IGNORECASE):
                structure_score += 10
                if structure_score >= 90:
                    break
        
        communication_score = structure_score + (good_count * 5) - (weak_count * 10)
        
        avg_word_length = sum(len(w) for w in answer.split()) / max(len(answer.split()), 1)
        if avg_word_length < 4:
            communication_score -= 10
        elif avg_word_length > 6:
            communication_score += 5
        
        return max(min(communication_score, 100), 0)
    
    def _generate_feedback(self, found: List[str], expected: List[str], comm_score: float) -> str:
        if not expected:
            return "Your answer was evaluated. Consider providing specific examples and details."
        
        coverage = len(found) / len(expected) * 100 if expected else 0
        
        if coverage >= 80 and comm_score >= 70:
            return "Excellent! You covered most key points effectively and communicated clearly."
        elif coverage >= 60:
            return "Good job! You addressed most key concepts. Consider adding more specific examples."
        elif coverage >= 40:
            return "You covered some important points. Try to include more technical details and examples."
        elif coverage >= 20:
            return "You mentioned a few key concepts. Try to be more comprehensive and provide examples."
        else:
            return "Consider studying the topic more thoroughly and providing specific examples and details."
    
    def _get_missing_points(self, found: List[str], expected: List[str]) -> List[str]:
        missing = []
        for keyword in expected:
            if keyword not in found:
                formatted = keyword.replace("_", " ").title()
                missing.append(f"Consider mentioning: {formatted}")
        
        return missing[:5]


answer_evaluator = AnswerEvaluator()
