import { useState } from 'react';
import type { Question, QuizResponse, AnswerSubmission } from '../types/quiz';

interface QuizDisplayProps {
  quiz: QuizResponse;
  onSubmit: (answers: AnswerSubmission[]) => void;
  onCancel: () => void;
}

export default function QuizDisplay({ quiz, onSubmit, onCancel }: QuizDisplayProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const handleOptionSelect = (questionId: string, optionId: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  const handleSubmit = () => {
    const submissions: AnswerSubmission[] = Object.entries(answers).map(
      ([question_id, selected_answer_id]) => ({
        question_id,
        selected_answer_id,
      })
    );
    onSubmit(submissions);
  };

  const allAnswered = quiz.questions.every((q) => answers[q.question_id]);
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h2>Quiz: {quiz.topic}</h2>
        <div className="quiz-progress">
          Progress: {answeredCount} / {quiz.questions.length} answered
        </div>
        {quiz.warning && (
          <div style={{ marginTop: '0.5rem', color: '#f59e0b' }}>
            ⚠️ Only {quiz.generated_questions} questions could be generated (requested {quiz.requested_questions})
          </div>
        )}
      </div>

      <div className="questions-list">
        {quiz.questions.map((question, index) => (
          <QuestionCard
            key={question.question_id}
            question={question}
            index={index}
            selectedAnswer={answers[question.question_id]}
            onSelect={(optionId) => handleOptionSelect(question.question_id, optionId)}
          />
        ))}
      </div>

      <div className="submit-section">
        <div className="form-actions">
          <button
            onClick={handleSubmit}
            className="btn-primary"
            disabled={!allAnswered}
          >
            Submit Quiz
          </button>
          <button onClick={onCancel} className="btn-secondary">
            Cancel
          </button>
        </div>
        {!allAnswered && (
          <p style={{ marginTop: '1rem', color: '#888' }}>
            Please answer all questions before submitting
          </p>
        )}
      </div>
    </div>
  );
}

interface QuestionCardProps {
  question: Question;
  index: number;
  selectedAnswer?: string;
  onSelect: (optionId: string) => void;
}

function QuestionCard({ question, index, selectedAnswer, onSelect }: QuestionCardProps) {
  return (
    <div className="question-card">
      <div className="question-number">Question {index + 1}</div>
      <div className="question-text">{question.text}</div>
      <div className="options">
        {question.options.map((option) => (
          <div
            key={option.id}
            className={`option ${selectedAnswer === option.id ? 'selected' : ''}`}
            onClick={() => onSelect(option.id)}
          >
            <span className="option-label">{option.id}.</span>
            {option.text}
          </div>
        ))}
      </div>
    </div>
  );
}
