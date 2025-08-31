'use client';

import { useChat } from '@ai-sdk/react';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import React, { useState } from 'react';

const ChatComponent = () => {
  const { messages, sendMessage, status, stop, addToolResult } = useChat({
    onToolCall: async ({ toolCall }) => {
      // Note: do not await addToolResult to avoid deadlocks
      try {
        // Ignore dynamic tools for type safety
        if ((toolCall as any).dynamic) return;

        const baseUrl = new URL(window.location.origin + '/api/mcp-server');
        const transport = new StreamableHTTPClientTransport(baseUrl);
        const client = new Client({ name: 'web-client', version: '1.0.0' });
        await client.connect(transport);

        const result = await client.callTool({ 
          name: toolCall.toolName, 
          arguments: toolCall.args 
        });
        
        addToolResult({
          tool: toolCall.toolName,
          toolCallId: (toolCall as any).toolCallId,
          output: result.content,
        });
      } catch (err) {
        console.error('MCP tool call failed:', err);
        addToolResult({
          tool: toolCall.toolName,
          toolCallId: (toolCall as any).toolCallId,
          output: [{ type: 'text', text: 'Tool error: unable to execute MCP call.' }],
        });
      }
    },
  });

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