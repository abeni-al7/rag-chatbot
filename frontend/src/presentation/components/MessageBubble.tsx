import React from 'react';
import { Message } from '../../domain/types';
import { FileText, User, Bot } from 'lucide-react';

interface MessageBubbleProps {
    message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-2`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    isUser ? 'bg-blue-600 text-white' : 'bg-emerald-600 text-white'
                }`}>
                    {isUser ? <User size={16} /> : <Bot size={16} />}
                </div>

                {/* Message Content */}
                <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                    <div className={`px-4 py-2 rounded-2xl ${
                        isUser 
                            ? 'bg-blue-600 text-white rounded-tr-none' 
                            : 'bg-gray-100 text-gray-800 rounded-tl-none'
                    }`}>
                        <p className="whitespace-pre-wrap text-sm leading-relaxed">
                            {message.content}
                        </p>
                    </div>

                    {/* Citations */}
                    {!isUser && message.citations && message.citations.length > 0 && (
                        <div className="mt-2 space-y-1">
                            <p className="text-xs font-semibold text-gray-500 ml-1">Sources:</p>
                            <div className="flex flex-wrap gap-2">
                                {message.citations.map((citation, index) => (
                                    <div 
                                        key={index}
                                        className="flex items-center gap-1 px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-600 hover:bg-gray-50 transition-colors"
                                        title={`Page ${citation.page}`}
                                    >
                                        <FileText size={10} />
                                        <span className="max-w-[150px] truncate">{citation.source}</span>
                                        <span className="text-gray-400">p.{citation.page}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
