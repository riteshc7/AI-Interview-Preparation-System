from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    QuestionGenerateRequest,
    QuestionGenerateResponse,
    EvaluateAnswerRequest,
    EvaluationResponse
)
from ..services.question_generator import question_generator
from ..services.answer_evaluator import answer_evaluator

router = APIRouter(prefix="/ai", tags=["AI Services"])


@router.post("/generate-questions/", response_model=QuestionGenerateResponse)
async def generate_questions(request: QuestionGenerateRequest):
    try:
        questions = question_generator.generate(request)
        return QuestionGenerateResponse(questions=questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question generation failed: {str(e)}")


@router.post("/evaluate-answer/", response_model=EvaluationResponse)
async def evaluate_answer(request: EvaluateAnswerRequest):
    try:
        result = answer_evaluator.evaluate(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
