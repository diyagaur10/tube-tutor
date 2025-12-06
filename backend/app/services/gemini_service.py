import json
from typing import Dict, Any
# from app.config import settings
from google import genai
from google.genai.errors import APIError
import os
import time

# # Initialize the Gemini Client. It automatically picks up the GEMINI_API_KEY.
# try:
#     client = genai.Client()
# except Exception as e:
#     # Client will be None if the key is not available, requiring fallback logic
#     client = None 

# MODEL = "gemini-2.5-flash" 
# JSON_CONFIG = genai.types.GenerateContentConfig(
#     response_mime_type="application/json",
# )


class GeminiService:

    @staticmethod
    def _get_client_or_fallback():
        """Helper to safely initialize and return the Gemini client."""
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("FATAL: Key missing in runtime environment.")
            return None
        
        cleaned_api_key = api_key.strip().strip('"').strip("'")
        
        # We must check the cleaned key is not empty
        if not cleaned_api_key:
            print("FATAL: Key was found but was empty after stripping quotes.")
            return None

        # Print the result of the stripping for final diagnostic, if necessary
        print(f"DIAGNOSTIC: Cleaned Key Length: {len(cleaned_api_key)}")

        # Use the cleaned key for initialization
        return genai.Client(api_key=cleaned_api_key)

    @staticmethod
    def generate_question(transcript_segment: str, timestamp: float, question_type: str) -> Dict[str, Any]:
        """Generates a question (MCQ, fill_in, etc.) and options based on a transcript segment."""
        MODEL = "gemini-2.5-flash" 
        JSON_CONFIG = genai.types.GenerateContentConfig(
            response_mime_type="application/json",
        )
        client = GeminiService._get_client_or_fallback()
        # if not client:
        #     # Fallback for uninitialized client
        #     return {
        #         "question_text": f"Fallback: What is the main topic discussed at the {int(timestamp)}s mark?",
        #         "options": ["Topic A", "Topic B", "Topic C", "Topic D"] if question_type == "mcq" else [],
        #         "correct_answer": "Topic A",
        #         "explanation": "Service unavailable: Gemini client not initialized."
        #     }
        
        #Trying to find the error, if client is initialized or not?
        if client is None:
            return {
                "question_text": f"FATAL ERROR: Client could not initialize for question at {int(timestamp)}s.",
                "options": ["Check .env", "Check Docker-Compose", "Check Quota", "Check Firewall"], 
                "correct_answer": "Check .env",
                "explanation": "Client failed to initialize. Review container logs for specific API error details."
            }
            
        prompt = f"""
        Generate a {question_type} question based on the following text content, which covers material up to {timestamp} seconds into a lecture.
        
        Text Content: {transcript_segment}
        
        Requirements:
        1. The question must test understanding of a key concept in the text.
        2. For MCQ, provide exactly 4 options with only one correct answer.
        3. Keep the explanation concise and clear.
        
        Return the result as a single JSON object (no markdown or extra text):
        {{
            "question_text": "string (the question)",
            "options": ["option1", "option2", "option3", "option4"], 
            "correct_answer": "string (the text of the correct option)",
            "explanation": "string (brief explanation)"
        }}
        """
        
        # response = client.generate_content(
        #         model=MODEL,
        #         contents=[prompt],
        #         config=JSON_CONFIG,
        #     )
        # return json.loads(response.text)
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt],
                config=JSON_CONFIG,
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Call Failed: {e}")
            # Fallback for API call error
            return {
                "question_text": f"API Error Fallback: What is the main topic at {int(timestamp)}s?",
                "options": ["Topic A", "Topic B", "Topic C", "Topic D"] if question_type == "mcq" else [],
                "correct_answer": "Topic A",
                "explanation": "Question generation failed due to service error."
            }

    @staticmethod
    def grade_answer(question: str, user_answer: str, correct_answer: str) -> Dict[str, Any]:
        """Grades a user's answer against the correct answer and provides an explanation."""
        MODEL = "gemini-2.5-flash" 
        JSON_CONFIG = genai.types.GenerateContentConfig(
            response_mime_type="application/json",
        )
        client = GeminiService._get_client_or_fallback()
        # if not client:
        #     is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
        #     return {
        #         "correct": is_correct,
        #         "explanation": "Service unavailable. Grading based on simple string match." if not is_correct else "Answer correct.",
        #         "hint": ""
        #     }
            
        prompt = f"""
        Grade the user's answer. 
        
        Question: {question}
        Correct Answer: {correct_answer}
        User Answer: {user_answer}
        
        Instructions:
        1. Respond with a boolean for the 'correct' field.
        2. Provide a brief explanation for why the answer is correct or incorrect.
        3. Be lenient with minor spelling or formatting variations.
        
        Return JSON (no markdown):
        {{
            "correct": boolean,
            "explanation": "string (brief feedback)",
            "hint": "string (optional hint for incorrect answer)"
        }}
        """
        
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt],
                config=JSON_CONFIG,
            )
            return json.loads(response.text)
        except Exception as e:
            # Fallback for API call error
            is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
            return {
                "correct": is_correct,
                "explanation": "Grading API failed. Simple string match used." if not is_correct else "Answer correct.",
                "hint": "Review the video content."
            }

    @staticmethod
    def generate_summary(transcript_segment: str, failed_question: str) -> str:
        """Generates a brief summary when a student fails all attempts."""
        MODEL = "gemini-2.5-flash" 
        JSON_CONFIG = genai.types.GenerateContentConfig(
            response_mime_type="application/json",
        )
        client = GeminiService._get_client_or_fallback()
        # if not client:
        #     return "Please review the video content to better understand the concepts discussed."
            
        prompt = f"""
        The student failed the question: "{failed_question}".
        
        Based on the content segment: {transcript_segment}
        
        Provide a concise summary (2-3 sentences) of the core concepts in the text that would help the student answer the question. Keep it encouraging.
        """
        
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt],
            )
            return response.text.strip()
        except Exception as e:
            return "Summary generation failed. Please review the video content."
    
    @staticmethod
    def generate_transcript(video_path: str) -> str | None:
        """Uploads a video file and requests a full transcript from the Gemini API."""
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return None
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable is not set.")
            return None

        client = genai.Client(api_key=api_key)
        file = None
        try:
            # 1. Upload the file to the Gemini API
            print(f"Uploading file: {video_path}...")
            file = client.files.upload(file=video_path)

            # --- GUARANTEED POLLING FIX ---
            print(f"Waiting for file {file.name} to become active...")
            
            # Poll the file status, waiting up to 5 minutes (300 seconds)
            timeout = time.time() + 300 
            
            # Get the initial file object with the 'state' property
            current_file = client.files.get(name=file.name)
            
            while current_file.state.name != "ACTIVE" and time.time() < timeout:
                # Check the file state every 5 seconds
                time.sleep(5) 
                current_file = client.files.get(name=file.name)

                if current_file.state.name == "FAILED":
                    print(f"File processing failed: {current_file.error.message}")
                    client.files.delete(name=current_file.name)
                    return None
            
            if current_file.state.name != "ACTIVE":
                print("Error: File did not become active within the timeout period.")
                client.files.delete(name=current_file.name)
                return None
            # --- END GUARANTEED POLLING FIX ---

            # print(f"Waiting for file {file.name} to become active...")
            # # Poll the file status, waiting up to 5 minutes (300 seconds)
            # timeout = time.time() + 300 
            # while file.state.name != "ACTIVE" and time.time() < timeout:
            #     file = client.files.get(name=file.name)
            #     if file.state.name == "FAILED":
            #         print(f"File processing failed: {file.error.message}")
            #         client.files.delete(name=file.name)
            #         return None
            #     if file.state.name != "ACTIVE":
            #         time.sleep(5) # Wait 5 seconds before checking again
            
            # if file.state.name != "ACTIVE":
            #     print("Error: File did not become active within the timeout period.")
            #     client.files.delete(name=file.name)
            #     return None

            # 2. Call the model to transcribe the video
            print("Requesting transcription...")
            response = client.models.generate_content(
                model='gemini-2.5-flash', # Or a model optimized for long context/video
                contents=[
                    file,
                    "Provide a complete, accurate, and time-stamped transcript of the entire video. Focus on the spoken content and do not include any introductory or concluding remarks about the transcription process itself."
                ],
            )
            
            # 3. Clean up the uploaded file (Best practice to clean up API files immediately)
            client.files.delete(name=file.name)
            
            return response.text.strip()
            
        except APIError as e:
            print(f"Gemini API Error during transcription: {e}")
            if file:
                client.files.delete(name=file.name)
            return None
        except Exception as e:
            print(f"An unexpected error occurred during transcription: {e}")
            return None