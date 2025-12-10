import { useState, useCallback } from 'react';
import type { Message, ChatState } from '../../domain/types';
import { sendQuery } from '../../data/api';

export const useChat = () => {
    const [state, setState] = useState<ChatState>({
        messages: [],
        isLoading: false,
        error: null,
    });

    const sendMessage = useCallback(async (content: string) => {
        // Add user message immediately
        const userMessage: Message = { role: 'user', content };
        
        setState(prev => ({
            ...prev,
            messages: [...prev.messages, userMessage],
            isLoading: true,
            error: null,
        }));

        try {
            // Send query to backend with history
            const response = await sendQuery(content, state.messages);

            // Add assistant response
            const assistantMessage: Message = {
                role: 'assistant',
                content: response.answer,
                citations: response.citations,
            };

            setState(prev => ({
                ...prev,
                messages: [...prev.messages, assistantMessage],
                isLoading: false,
            }));
        } catch (error) {
            setState(prev => ({
                ...prev,
                isLoading: false,
                error: 'Failed to get response. Please try again.',
            }));
            console.error('Chat error:', error);
        }
    }, [state.messages]);

    const clearChat = useCallback(() => {
        setState({
            messages: [],
            isLoading: false,
            error: null,
        });
    }, []);

    return {
        messages: state.messages,
        isLoading: state.isLoading,
        error: state.error,
        sendMessage,
        clearChat,
    };
};
