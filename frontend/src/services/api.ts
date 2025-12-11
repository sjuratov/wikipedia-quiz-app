import axios from 'axios';
import type { QuizRequest, QuizResponse, SubmitRequest, SubmitResponse } from '../types/quiz';

const API_BASE_URL = '/api';

export const quizApi = {
  async generateQuiz(request: QuizRequest): Promise<QuizResponse> {
    const response = await axios.post<QuizResponse>(
      `${API_BASE_URL}/quiz/generate`,
      request
    );
    return response.data;
  },

  async submitQuiz(request: SubmitRequest): Promise<SubmitResponse> {
    const response = await axios.post<SubmitResponse>(
      `${API_BASE_URL}/quiz/submit`,
      request
    );
    return response.data;
  },

  async healthCheck(): Promise<any> {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }
};
