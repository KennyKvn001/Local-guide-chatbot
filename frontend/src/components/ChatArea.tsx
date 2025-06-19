import { useState } from "react";
import { Send, MapPin } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export function ChatArea() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hello! 👋 I'm LocalGuide, your personal AI chatbot for discovering amazing local places and experiences in Rwanda. How can I assist you today?",
      sender: 'bot',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    const userText = inputValue.trim();

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content: userText,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    // Placeholder bot message while waiting
    const loadingId = (Date.now() + 1).toString();
    setMessages((prev) => [
      ...prev,
      {
        id: loadingId,
        content: "…",
        sender: 'bot',
        timestamp: new Date(),
      },
    ]);

    // Call backend
    fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: userText }),
    })
      .then(async (res) => {
        if (!res.ok) {
          const data = await res.json().catch(() => null);
          throw new Error(data?.detail || res.statusText);
        }
        return res.json();
      })
      .then((data) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === loadingId ? { ...m, content: data.response } : m
          )
        );
      })
      .catch((err) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === loadingId
              ? { ...m, content: `Error: ${err.message}` }
              : m
          )
        );
      });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 mb-20">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                message.sender === 'user'
                  ? 'bg-gradient-to-r from-blue-500 to-green-500 text-white'
                  : 'bg-white border border-gray-200 text-gray-900'
              }`}
            >
              {message.sender === 'bot' && (
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-green-500 rounded-full flex items-center justify-center">
                    <MapPin className="w-3 h-3 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-600">LocalGuide</span>
                </div>
              )}
              <p className="text-sm leading-relaxed">{message.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4 sticky bottom-0 w-full">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about local places, restaurants, activities..."
              className="w-full resize-none rounded-2xl border border-gray-200 px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              rows={1}
              style={{ minHeight: '44px', maxHeight: '120px' }}
            />
          </div>
          <Button
            onClick={handleSendMessage}
            disabled={!inputValue.trim()}
            className="h-11 w-11 rounded-2xl bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600 disabled:opacity-50 p-0"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
