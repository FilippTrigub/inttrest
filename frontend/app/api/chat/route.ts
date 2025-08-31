import { streamText, convertToModelMessages, UIMessage } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

export const maxDuration = 30;

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json();
    
    const result = await streamText({
      model: openai('gpt-4o'),
      system: 'You are a helpful and friendly chatbot who assists users with their questions about maps and geography.',
      messages: convertToModelMessages(messages),
      tools: {
        search_places: {
          description: 'Search points of interest by category and optional date',
          parameters: z.object({
            category: z.string(),
            date: z.string().optional(),
          }),
          // No execute: handled client-side via MCP onToolCall
        },
      },
    });
    
    return result.toUIMessageStreamResponse();
  } catch (error) {
    console.error('Error in chat API route:', error);
    return new Response(
      JSON.stringify({ error: 'An error occurred while processing your request' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}