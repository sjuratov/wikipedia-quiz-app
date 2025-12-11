import type { SubmitResponse } from '../types/quiz';

interface ResultsDisplayProps {
  results: SubmitResponse;
  onNewQuiz: () => void;
}

export default function ResultsDisplay({ results, onNewQuiz }: ResultsDisplayProps) {
  const { score, results: quizResults } = results;

  const getScoreColor = () => {
    if (score.percentage >= 80) return '#10b981';
    if (score.percentage >= 60) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <div className="results-container">
      <div className="score-summary">
        <h2>{score.correct} / {score.total}</h2>
        <div className="score-percentage" style={{ color: getScoreColor() }}>
          {score.percentage.toFixed(1)}% Correct
        </div>
      </div>

      <div className="results-list">
        {quizResults.map((result, index) => (
          <div
            key={result.question_id}
            className={`result-item ${result.is_correct ? 'correct' : 'incorrect'}`}
          >
            <div className="result-header">
              <span className={`result-status ${result.is_correct ? 'correct' : 'incorrect'}`}>
                {result.is_correct ? '✓ Correct' : '✗ Incorrect'}
              </span>
              <span style={{ color: '#888' }}>Question {index + 1}</span>
            </div>

            <div className="result-question">{result.question_text}</div>

            <div className="result-answers">
              {!result.is_correct && (
                <div className="result-answer incorrect-answer">
                  Your answer: {result.selected_answer_id}. {result.selected_answer_text}
                </div>
              )}
              <div className="result-answer correct-answer">
                Correct answer: {result.correct_answer_id}. {result.correct_answer_text}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="submit-section">
        <button onClick={onNewQuiz} className="btn-primary">
          Take Another Quiz
        </button>
      </div>
    </div>
  );
}
