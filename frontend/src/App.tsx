import { useState } from 'react';
import './App.css';
import QuizForm from './components/QuizForm';
import QuizDisplay from './components/QuizDisplay';
import ResultsDisplay from './components/ResultsDisplay';
import { quizApi } from './services/api';
import type { QuizRequest, QuizResponse, SubmitRequest, SubmitResponse, AnswerSubmission } from './types/quiz';

type AppState = 'form' | 'loading' | 'quiz' | 'results' | 'error';

function App() {
  const [state, setState] = useState<AppState>('form');
  const [quiz, setQuiz] = useState<QuizResponse | null>(null);
  const [results, setResults] = useState<SubmitResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleGenerateQuiz = async (request: QuizRequest) => {
    setState('loading');
    setError('');

    try {
      const response = await quizApi.generateQuiz(request);
      setQuiz(response);
      setState('quiz');
    } catch (err: any) {
      console.error('Quiz generation error:', err);
      
      let errorMessage = 'Failed to generate quiz. Please try again.';
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail;
        if (typeof detail === 'object') {
          errorMessage = detail.message || errorMessage;
        } else {
          errorMessage = detail;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setState('error');
    }
  };

  const handleSubmitQuiz = async (answers: AnswerSubmission[]) => {
    if (!quiz) return;

    setState('loading');
    setError('');

    try {
      const request: SubmitRequest = {
        quiz_id: quiz.quiz_id,
        answers,
      };
      const response = await quizApi.submitQuiz(request);
      setResults(response);
      setState('results');
    } catch (err: any) {
      console.error('Quiz submission error:', err);
      setError('Failed to submit quiz. Please try again.');
      setState('error');
    }
  };

  const handleNewQuiz = () => {
    setQuiz(null);
    setResults(null);
    setError('');
    setState('form');
  };

  const handleCancel = () => {
    handleNewQuiz();
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📚 Wikipedia Quiz</h1>
        <p>Test your knowledge on any topic</p>
      </header>

      <main>
        {state === 'form' && (
          <QuizForm onSubmit={handleGenerateQuiz} isLoading={false} />
        )}

        {state === 'loading' && (
          <div className="loading">
            <div className="spinner"></div>
            <p>
              {quiz 
                ? 'Submitting your answers...' 
                : 'Generating your quiz... This may take a few seconds.'}
            </p>
          </div>
        )}

        {state === 'quiz' && quiz && (
          <QuizDisplay
            quiz={quiz}
            onSubmit={handleSubmitQuiz}
            onCancel={handleCancel}
          />
        )}

        {state === 'results' && results && (
          <ResultsDisplay results={results} onNewQuiz={handleNewQuiz} />
        )}

        {state === 'error' && (
          <div>
            <div className="error">
              <h3>⚠️ Error</h3>
              <p>{error}</p>
            </div>
            <div className="form-actions" style={{ marginTop: '2rem' }}>
              <button onClick={handleNewQuiz} className="btn-primary">
                Try Again
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
