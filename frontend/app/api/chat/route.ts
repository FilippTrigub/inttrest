import { streamText, convertToModelMessages, UIMessage, experimental_createMCPClient, stepCountIs } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';

export const maxDuration = 30;

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json();

    // Connect to the MCP server and fetch tools dynamically
    const mcpClient = await experimental_createMCPClient({
      transport: new StreamableHTTPClientTransport(new URL('http://127.0.0.1:8000/mcp')),
    });
    const tools = await mcpClient.tools();
    // Log discovered tools for verification
    console.log('MCP tools discovered:', Object.keys(tools));

    const result = await streamText({
      model: openai('gpt-4.1'),
      system: 'You are a helpful assistant for maps, geography, and information lookup. When relevant, proactively use the available tools to search, retrieve, or analyze data before answering. Prefer tool usage for up-to-date information, geographic data, or structured lookups.',
      messages: convertToModelMessages(messages),
      tools,
      toolChoice: 'required',
      // Limit to a single tool-calling step
      stopWhen: stepCountIs(1),
      onStepFinish: async ({ toolCalls, toolResults, text, finishReason, usage }) => {
        if (toolCalls?.length) {
          console.log('Tool calls:', JSON.stringify(toolCalls, null, 2));
        }
        if (toolResults?.length) {
          console.log('Tool results:', JSON.stringify(toolResults, null, 2));
        }
      },
      onFinish: async () => {
        await mcpClient.close();
      },
      onError: async () => {
        await mcpClient.close();
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