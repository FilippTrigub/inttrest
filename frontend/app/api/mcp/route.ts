import { createMcpHandler } from '@vercel/mcp-adapter';
import { z } from 'zod';

const handler = createMcpHandler(
  (server) => {
    server.tool(
      'search_places',
      'Search points of interest by category and optional date',
      {
        category: z.string(),
        date: z.string().optional(),
      },
      async ({ category, date }) => {
        const when = date ? ` on ${date}` : '';
        return {
          content: [
            {
              type: 'text',
              text: `Searched for category "${category}"${when}. (Demo response)`,
            },
          ],
        };
      }
    );
  },
  {
    // Server options (none for now)
  },
  {
    basePath: '/api',
    verboseLogs: true,
  }
);

export { handler as GET, handler as POST };


