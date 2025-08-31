'use client';

import { useChat } from '@ai-sdk/react';
import React, { useState, useEffect, useRef } from 'react';

interface ChatComponentProps {
  onStreamingFinished?: () => void;
}

const ChatComponent = ({ onStreamingFinished }: ChatComponentProps) => {
  const { messages, sendMessage, status, stop } = useChat();

  const categories = [
    'Restaurants',
    'Parcs',
    'Musées',
    'Cafés',
    'Shopping',
    'Hôtels',
  ];

  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [date, setDate] = useState<string>('');

  const toggleCategory = (category: string) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((c) => c !== category)
        : [...prev, category]
    );
  };

  const [textInput, setTextInput] = useState<string>('');
  const previousStatus = useRef(status);

  // Monitor status changes to trigger callback when streaming finishes
  useEffect(() => {
    if (previousStatus.current === 'streaming' && status === 'ready') {
      onStreamingFinished?.();
    }
    previousStatus.current = status;
  }, [status, onStreamingFinished]);

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const trimmed = textInput.trim();
    if (!trimmed) return;
    sendMessage({ text: trimmed });
    setTextInput('');
  };

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-gray-600">
        <div className="mb-4">
          <div className="text-sm text-gray-300 mb-2">Catégories</div>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => {
              const isSelected = selectedCategories.includes(category);
              return (
                <button
                  type="button"
                  key={category}
                  onClick={() => toggleCategory(category)}
                  className={
                    `px-3 py-1 rounded-full text-sm border transition-colors ` +
                    (isSelected
                      ? 'bg-blue-600 border-blue-600 text-white'
                      : 'bg-gray-800 border-gray-600 text-gray-200 hover:bg-gray-700')
                  }
                >
                  {category}
                </button>
              );
            })}
          </div>
        </div>
        <div>
          <div className="text-sm text-gray-300 mb-2">Date</div>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="w-full p-2 rounded-md bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`p-3 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-600 self-end'
                : 'bg-gray-700 self-start'
            }`}
          >
            <div className="font-semibold">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div className="mt-2">
              {message.parts.map((part, index) => {
                switch (part.type) {
                  case 'text':
                    return <div key={index}>{part.text}</div>;
                  default:
                    if (typeof part.type === 'string' && part.type.startsWith('tool-')) {
                      console.log('Tool Part:', part);
                      const toolName = (part as any).toolName || part.type.slice('tool-'.length);
                      const state = (part as any).state;
                      if (state === 'input-available') {
                        return (
                          <div key={index} className="text-sm text-gray-200">
                            Appel de l'outil {toolName} avec les arguments :{' '}
                            <pre className="whitespace-pre-wrap break-all inline">
                              {JSON.stringify((part as any).input, null, 2)}
                            </pre>
                          </div>
                        );
                      }
                      if (state === 'output-available') {
                        return (
                          <div key={index} className="text-sm text-gray-200">
                            Résultat de l'outil :{' '}
                            <pre className="whitespace-pre-wrap break-all inline">
                              {JSON.stringify((part as any).output, null, 2)}
                            </pre>
                          </div>
                        );
                      }
                      if (state === 'output-error') {
                        return (
                          <div key={index} className="text-sm text-red-300">
                            Erreur de l'outil : {(part as any).errorText}
                          </div>
                        );
                      }
                      // For other tool states like input-streaming, etc., show a compact placeholder
                      return (
                        <div key={index} className="text-sm text-gray-400">
                          Outil {toolName} • état: {String(state)}
                        </div>
                      );
                    }
                    return null;
                }
              })}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={onSubmit} className="p-4 border-t border-gray-600">
        <input
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          className="w-full p-2 rounded-md bg-gray-800 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type your message..."
          disabled={status !== 'ready'}
        />
        <div className="mt-2 flex gap-2">
          <button
            type="submit"
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-60"
            disabled={status !== 'ready'}
          >
            Send
          </button>
          {(status === 'submitted' || status === 'streaming') && (
            <button
              type="button"
              onClick={() => stop?.()}
              className="px-4 py-2 rounded bg-gray-700 border border-gray-600 text-white"
            >
              Stop
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default ChatComponent;