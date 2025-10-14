import openai
import json
from typing import Dict, Any
from app.config import settings

openai.api_key = settings.openai_api_key

class OpenAIService:
    @staticmethod
    def generate_question(transcript_segment: str, timestamp: float, question_type: str) -> Dict[str, Any]:
        prompt = f"""
        Based on the video transcript up to timestamp {timestamp} seconds, generate a {question_type} question.
        
        Transcript: {transcript_segment}
        
        Requirements:
        - Question should test understanding of key concepts mentioned
        - For MCQ: Provide 4 options with only one correct answer
        - For fill_in: Create a sentence with a blank to fill
        - For one_word: Ask for a specific term or concept
        - Make it challenging but fair based on the content shown
        
        Return JSON format:
        {{
            "question_text": "string",
            "options": ["option1", "option2", "option3", "option4"], // only for MCQ
            "correct_answer": "string",
            "explanation": "string"
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            # Fallback question if OpenAI fails
            return {
                "question_text": f"What is the main topic discussed in this video segment?",
                "options": ["Topic A", "Topic B", "Topic C", "Topic D"] if question_type == "mcq" else None,
                "correct_answer": "Main topic",
                "explanation": "This question tests understanding of the video content."
            }
    
    @staticmethod
    def grade_answer(question: str, user_answer: str, correct_answer: str) -> Dict[str, Any]:
        prompt = f"""
        Grade this answer for a learning video question.
        
        Question: {question}
        Correct Answer: {correct_answer}
        User Answer: {user_answer}
        
        Return JSON:
        {{
            "correct": boolean,
            "explanation": "Brief explanation of why the answer is correct/incorrect",
            "hint": "Optional hint for incorrect answers"
        }}
        
        Be lenient with minor variations in spelling/formatting for correct answers.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            # Simple string matching fallback
            is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            return {
                "correct": is_correct,
                "explanation": "Answer is correct." if is_correct else "Answer is incorrect.",
                "hint": "Please review the video content." if not is_correct else None
            }
    
    @staticmethod
    def generate_summary(transcript_segment: str, failed_question: str) -> str:
        prompt = f"""
        The student failed to answer this question correctly: {failed_question}
        
        Based on the video content up to this point, provide a brief summary (2-3 sentences) 
        that helps the student understand the key concepts they need to know.
        
        Transcript segment: {transcript_segment}
        
        Focus on the most important points that would help answer the question correctly.
        Keep it concise and encouraging.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "Please review the video content to better understand the concepts discussed."
