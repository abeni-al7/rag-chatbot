import axios from 'axios';
import type { Message, Citation } from '../domain/types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const uploadDocument = async (file: File): Promise<void> => {
    const formData = new FormData();
    formData.append('file', file);
    await api.post('/ingest', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

interface ChatResponse {
    answer: string;
    citations: { source: string; page_number: number }[];
}

export const sendQuery = async (query: string, history: Message[] = []): Promise<{ answer: string; citations: Citation[] }> => {
    // Filter out citations from history messages before sending to backend
    const cleanHistory = history.map(({ role, content }) => ({ role, content }));

    const response = await api.post<ChatResponse>('/chat', {
        query,
        history: cleanHistory,
    });

    return {
        answer: response.data.answer,
        citations: response.data.citations.map((c) => ({
            source: c.source,
            page: c.page_number,
        })),
    };
};
