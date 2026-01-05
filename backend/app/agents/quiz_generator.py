"""LangGraph-based agent for quiz generation."""
import os
import json
import random
from typing import TypedDict, List, Optional, Dict, Any, Annotated
from operator import add

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from app.services.wikipedia_client import wikipedia_client
from app.models.quiz import Question, Option


class QuizGenerationState(TypedDict):
    """State for the quiz generation pipeline."""
    topic: str
    num_questions: int
    resolved_topic: Optional[str]
    wikipedia_content: Optional[str]
    raw_questions: Optional[List[Dict[str, Any]]]
    validated_questions: Annotated[List[Question], add]
    errors: Annotated[List[str], add]
    metadata: Dict[str, Any]


class QuizGenerationAgent:
    """Agent pipeline for generating quizzes from Wikipedia content."""
    
    def __init__(self):
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not all([azure_endpoint, api_key, deployment_name]):
            raise ValueError("Azure OpenAI environment variables not set (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME)")
            
        self.llm = AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
            deployment_name=deployment_name,
            temperature=0.7
        )
        
        # Build the graph
        workflow = StateGraph(QuizGenerationState)
        
        # Add nodes
        workflow.add_node("resolve_topic", self.resolve_topic)
        workflow.add_node("extract_content", self.extract_content)
        workflow.add_node("generate_questions", self.generate_questions)
        workflow.add_node("validate_questions", self.validate_questions)
        
        # Set entry point
        workflow.set_entry_point("resolve_topic")
        
        # Add edges
        workflow.add_edge("resolve_topic", "extract_content")
        workflow.add_edge("extract_content", "generate_questions")
        workflow.add_edge("generate_questions", "validate_questions")
        workflow.add_edge("validate_questions", END)
        
        self.graph = workflow.compile()
        
    async def resolve_topic(self, state: QuizGenerationState) -> Dict[str, Any]:
        """Node 1: Resolve and disambiguate the topic."""
        topic = state["topic"]
        
        # Search Wikipedia for the topic
        results = await wikipedia_client.search_topic(topic, limit=3)
        
        if not results:
            return {
                "errors": [f"No Wikipedia articles found for topic: {topic}"],
                "metadata": {"stage": "topic_resolution", "success": False}
            }
        
        # Use the first result
        resolved_title = results[0]["title"]
        
        return {
            "resolved_topic": resolved_title,
            "metadata": {"stage": "topic_resolution", "success": True, "candidates": len(results)}
        }
        
    async def extract_content(self, state: QuizGenerationState) -> Dict[str, Any]:
        """Node 2: Extract Wikipedia content."""
        resolved_topic = state.get("resolved_topic")
        
        if not resolved_topic:
            return {
                "errors": ["No resolved topic available"],
                "metadata": {"stage": "content_extraction", "success": False}
            }
        
        # Get article content
        content = await wikipedia_client.get_article_content(resolved_topic)
        
        if not content:
            return {
                "errors": [f"Could not retrieve content for: {resolved_topic}"],
                "metadata": {"stage": "content_extraction", "success": False}
            }
        
        # Check if content is sufficient (at least 200 words for minimal quiz)
        word_count = len(content.split())
        if word_count < 200:
            return {
                "errors": [f"Insufficient content (only {word_count} words)"],
                "metadata": {"stage": "content_extraction", "success": False, "word_count": word_count}
            }
        
        # Truncate to first 3000 words to fit in context
        words = content.split()
        if len(words) > 3000:
            content = " ".join(words[:3000])
        
        return {
            "wikipedia_content": content,
            "metadata": {"stage": "content_extraction", "success": True, "word_count": len(content.split())}
        }
        
    async def generate_questions(self, state: QuizGenerationState) -> Dict[str, Any]:
        """Node 3: Generate quiz questions using Claude."""
        content = state.get("wikipedia_content")
        num_questions = state["num_questions"]
        topic = state.get("resolved_topic", state["topic"])
        
        if not content:
            return {
                "errors": ["No content available for question generation"],
                "metadata": {"stage": "question_generation", "success": False}
            }
        
        system_prompt = """You are an expert quiz creator. Generate multiple-choice questions based on the provided Wikipedia content.

Requirements for each question:
1. The question must be directly answerable from the provided content
2. Create exactly 4 answer options (A, B, C, D)
3. Only ONE option should be correct
4. The three incorrect options (distractors) should be plausible but clearly wrong
5. Questions should test factual understanding
6. Avoid questions that require memorizing long lists
7. Make questions clear and unambiguous
8. Identify the Wikipedia section heading where the answer is found (if determinable)

Return your response as a JSON array of questions, where each question has this structure:
{
    "text": "The question text",
    "options": [
        {"id": "A", "text": "Option A text"},
        {"id": "B", "text": "Option B text"},
        {"id": "C", "text": "Option C text"},
        {"id": "D", "text": "Option D text"}
    ],
    "correct_answer_id": "A",
    "section_heading": "Section Name" (optional - include if the answer is found in a specific section)
}

IMPORTANT: Return ONLY the JSON array, no other text or formatting."""

        user_prompt = f"""Topic: {topic}

Content:
{content}

Generate exactly {num_questions} multiple-choice questions based on this content. Return only the JSON array."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            response_text = response.content.strip()
            
            # Try to extract JSON from response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            questions = json.loads(response_text)
            
            if not isinstance(questions, list):
                return {
                    "errors": ["Generated response is not a list of questions"],
                    "metadata": {"stage": "question_generation", "success": False}
                }
            
            return {
                "raw_questions": questions,
                "metadata": {"stage": "question_generation", "success": True, "count": len(questions)}
            }
            
        except json.JSONDecodeError as e:
            return {
                "errors": [f"Failed to parse generated questions: {str(e)}"],
                "metadata": {"stage": "question_generation", "success": False}
            }
        except Exception as e:
            return {
                "errors": [f"Question generation failed: {str(e)}"],
                "metadata": {"stage": "question_generation", "success": False}
            }
    
    async def validate_questions(self, state: QuizGenerationState) -> Dict[str, Any]:
        """Node 4: Validate and structure questions."""
        raw_questions = state.get("raw_questions", [])
        resolved_topic = state.get("resolved_topic", state["topic"])
        
        if not raw_questions:
            return {
                "errors": ["No questions to validate"],
                "metadata": {"stage": "validation", "success": False}
            }
        
        validated = []
        
        for q_data in raw_questions:
            try:
                # Shuffle options to randomize correct answer position
                options = q_data.get("options", [])
                random.shuffle(options)
                
                # Construct reference URL
                reference_url = self._construct_reference_url(
                    resolved_topic,
                    q_data.get("section_heading")
                )
                
                question = Question(
                    text=q_data["text"],
                    options=[Option(**opt) for opt in options],
                    correct_answer_id=q_data["correct_answer_id"],
                    reference_url=reference_url
                )
                validated.append(question)
            except Exception as e:
                print(f"Skipping invalid question: {e}")
                continue
        
        return {
            "validated_questions": validated,
            "metadata": {"stage": "validation", "success": True, "validated_count": len(validated)}
        }
    
    def _construct_reference_url(self, article_title: str, section_heading: Optional[str] = None) -> str:
        """Construct Wikipedia reference URL with optional section anchor."""
        from urllib.parse import quote
        
        # Encode article title (replace spaces with underscores, URL encode special chars)
        encoded_title = article_title.replace(" ", "_")
        encoded_title = quote(encoded_title, safe="_")
        
        base_url = f"https://en.wikipedia.org/wiki/{encoded_title}"
        
        # Add section anchor if provided
        if section_heading:
            # Format section anchor (replace spaces with underscores)
            section_anchor = section_heading.replace(" ", "_")
            # URL encode special characters in the anchor
            section_anchor = quote(section_anchor, safe="_")
            return f"{base_url}#{section_anchor}"
        
        return base_url
    
    async def generate_quiz(self, topic: str, num_questions: int) -> Dict[str, Any]:
        """Run the complete quiz generation pipeline."""
        initial_state: QuizGenerationState = {
            "topic": topic,
            "num_questions": num_questions,
            "resolved_topic": None,
            "wikipedia_content": None,
            "raw_questions": None,
            "validated_questions": [],
            "errors": [],
            "metadata": {}
        }
        
        try:
            final_state = await self.graph.ainvoke(initial_state)
            return final_state
        except Exception as e:
            return {
                **initial_state,
                "errors": [f"Pipeline execution failed: {str(e)}"]
            }


# Global agent instance
quiz_agent = QuizGenerationAgent()
