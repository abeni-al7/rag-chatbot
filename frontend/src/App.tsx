import { Bot, Trash2 } from 'lucide-react';
import { FileUpload } from './presentation/components/FileUpload';
import { MessageBubble } from './presentation/components/MessageBubble';
import { ChatInput } from './presentation/components/ChatInput';
import { useChat } from './presentation/hooks/useChat';

function App() {
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar / Left Panel */}
      <div className="w-80 bg-white border-r border-gray-200 p-6 flex flex-col">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
            <Bot size={20} />
          </div>
          <h1 className="text-xl font-bold text-gray-800">RAG Chatbot</h1>
        </div>

        <div className="mb-6">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
            Documents
          </h2>
          <FileUpload />
        </div>

        <div className="mt-auto">
          <button
            onClick={clearChat}
            className="flex items-center gap-2 text-gray-500 hover:text-red-600 transition-colors text-sm font-medium"
          >
            <Trash2 size={16} />
            Clear Conversation
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-gray-400 mt-20">
                <Bot size={48} className="mb-4 opacity-20" />
                <p className="text-lg font-medium">No messages yet</p>
                <p className="text-sm">Upload a document and start asking questions!</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <MessageBubble key={index} message={msg} />
              ))
            )}
            
            {isLoading && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-2 flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}

            {error && (
              <div className="p-4 bg-red-50 text-red-600 rounded-lg text-center my-4">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <ChatInput onSend={sendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
}

export default App;
