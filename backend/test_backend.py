"""
Quick test script to verify the backend is working correctly.
Run this after starting the backend server.
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Health check passed: {data}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_generate_quiz():
    """Test quiz generation."""
    print("\n🎯 Testing quiz generation...")
    try:
        payload = {
            "topic": "Python programming language",
            "num_questions": 5
        }
        print(f"Request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/quiz/generate",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Quiz generated successfully!")
        print(f"Quiz ID: {data['quiz_id']}")
        print(f"Topic: {data['topic']}")
        print(f"Questions: {len(data['questions'])}")
        print(f"\nFirst question preview:")
        print(f"  {data['questions'][0]['text']}")
        for opt in data['questions'][0]['options']:
            print(f"    {opt['id']}. {opt['text']}")
        
        return data
    except requests.exceptions.Timeout:
        print("❌ Request timed out (this is normal for first request)")
        return None
    except Exception as e:
        print(f"❌ Quiz generation failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def test_submit_quiz(quiz_data):
    """Test quiz submission."""
    print("\n📝 Testing quiz submission...")
    try:
        # Create answers (selecting first option for each question)
        answers = [
            {
                "question_id": q["question_id"],
                "selected_answer_id": q["options"][0]["id"]
            }
            for q in quiz_data["questions"]
        ]
        
        payload = {
            "quiz_id": quiz_data["quiz_id"],
            "answers": answers
        }
        
        response = requests.post(
            f"{BASE_URL}/api/quiz/submit",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Quiz submitted successfully!")
        print(f"Score: {data['score']['correct']}/{data['score']['total']} ({data['score']['percentage']}%)")
        
        return True
    except Exception as e:
        print(f"❌ Quiz submission failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Wikipedia Quiz Application - Backend Test")
    print("=" * 60)
    
    # Test health check
    if not test_health_check():
        print("\n⚠️  Health check failed. Is the backend running?")
        print("Start it with: cd backend && python -m app.main")
        sys.exit(1)
    
    # Test quiz generation
    quiz_data = test_generate_quiz()
    if not quiz_data:
        print("\n⚠️  Quiz generation failed. Check:")
        print("1. ANTHROPIC_API_KEY is set in backend/.env")
        print("2. You have API credits")
        print("3. Backend logs for errors")
        sys.exit(1)
    
    # Test quiz submission
    if not test_submit_quiz(quiz_data):
        print("\n⚠️  Quiz submission failed.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! The backend is working correctly.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the frontend: cd frontend && npm run dev")
    print("2. Open http://localhost:5173 in your browser")
    print("3. Create and take quizzes!")

if __name__ == "__main__":
    main()
