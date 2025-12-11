import { useState } from 'react';
import type { QuizRequest } from '../types/quiz';

interface QuizFormProps {
  onSubmit: (request: QuizRequest) => void;
  isLoading: boolean;
}

export default function QuizForm({ onSubmit, isLoading }: QuizFormProps) {
  const [topic, setTopic] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topic.trim()) {
      onSubmit({ topic: topic.trim(), num_questions: numQuestions });
    }
  };

  return (
    <div className="quiz-form">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="topic">Quiz Topic</label>
          <input
            type="text"
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., Solar System, World War II, Leonardo da Vinci"
            required
            minLength={2}
            maxLength={200}
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="num_questions">Number of Questions</label>
          <select
            id="num_questions"
            value={numQuestions}
            onChange={(e) => setNumQuestions(Number(e.target.value))}
            disabled={isLoading}
          >
            {Array.from({ length: 18 }, (_, i) => i + 3).map((n) => (
              <option key={n} value={n}>
                {n} questions
              </option>
            ))}
          </select>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? 'Generating...' : 'Generate Quiz'}
          </button>
        </div>
      </form>
    </div>
  );
}
