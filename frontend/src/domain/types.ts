export interface Citation {
    source: string;
    page: number;
}

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    citations?: Citation[];
}

export interface ChatState {
    messages: Message[];
    isLoading: boolean;
    error: string | null;
}
