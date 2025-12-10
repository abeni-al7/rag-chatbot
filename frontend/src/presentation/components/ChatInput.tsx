import React, { useState, FormEvent } from 'react';
import { Send } from 'lucide-react';
import { Button } from './Button';

interface ChatInputProps {
    onSend: (message: string) => void;
    isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSend(input.trim());
            setInput('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="w-full bg-white border-t border-gray-100 p-4">
            <div className="flex items-center gap-2 max-w-4xl mx-auto">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about your documents..."
                    className="flex-1 px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    disabled={isLoading}
                />
                <Button 
                    type="submit" 
                    disabled={!input.trim() || isLoading}
                    className="!p-2 !rounded-full w-10 h-10 flex items-center justify-center"
                >
                    <Send size={18} />
                </Button>
            </div>
        </form>
    );
};
