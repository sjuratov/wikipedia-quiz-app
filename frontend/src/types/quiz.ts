export interface QuizRequest {
  topic: string;
  num_questions: number;
}

export interface Option {
  id: string;
  text: string;
}

export interface Question {
  question_id: string;
  text: string;
  options: Option[];
  correct_answer_id: string;
  reference_url?: string;
}

export interface QuizResponse {
  quiz_id: string;
  topic: string;
  questions: Question[];
  generated_at: string;
  warning?: string;
  requested_questions?: number;
  generated_questions?: number;
}

export interface AnswerSubmission {
  question_id: string;
  selected_answer_id: string;
}

export interface SubmitRequest {
  quiz_id: string;
  answers: AnswerSubmission[];
}

export interface QuizResult {
  question_id: string;
  question_text: string;
  selected_answer_id: string;
  selected_answer_text: string;
  correct_answer_id: string;
  correct_answer_text: string;
  is_correct: boolean;
  reference_url?: string;
}

export interface ScoreSummary {
  correct: number;
  total: number;
  percentage: number;
}

export interface SubmitResponse {
  quiz_id: string;
  score: ScoreSummary;
  results: QuizResult[];
  submitted_at: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: any;
}
