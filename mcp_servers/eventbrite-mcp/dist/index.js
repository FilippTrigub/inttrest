"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const dotenv_1 = __importDefault(require("dotenv"));
const zod_1 = require("zod");
// Load environment variables
dotenv_1.default.config();
// Import tool implementations
const listEvents_1 = require("./tools/events/listEvents");
const getEventDetails_1 = require("./tools/events/getEventDetails");
// Create MCP server
const server = new mcp_js_1.McpServer({
    name: process.env.MCP_SERVER_NAME || 'eventbrite',
    version: process.env.MCP_SERVER_VERSION || '0.1.0'
});
// Define event listing tool
server.tool('list_events', {
    status: zod_1.z.string().optional().describe('Filter by event status (draft, live, started, ended, completed, canceled)'),
    start_date: zod_1.z.string().optional().describe('Filter by start date (ISO 8601 format)'),
    end_date: zod_1.z.string().optional().describe('Filter by end date (ISO 8601 format)'),
    page: zod_1.z.number().optional().describe('Page number for pagination'),
    page_size: zod_1.z.number().optional().describe('Number of results per page')
}, async (args, extra) => {
    try {
        const result = await (0, listEvents_1.listEvents)(args);
        return {
            content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
    }
    catch (error) {
        console.error(`Error executing list_events:`, error);
        throw error;
    }
});
// Define event details tool
server.tool('get_event_details', {
    event_id: zod_1.z.string().describe('ID of the event to retrieve')
}, async (args, extra) => {
    try {
        const result = await (0, getEventDetails_1.getEventDetails)(args);
        return {
            content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
        };
    }
    catch (error) {
        console.error(`Error executing get_event_details:`, error);
        throw error;
    }
});
// Start the server
console.error('Starting Eventbrite MCP server...');
// Start receiving messages on stdin and sending messages on stdout
const transport = new stdio_js_1.StdioServerTransport();
server.connect(transport).catch(error => {
    console.error('Error connecting to transport:', error);
    process.exit(1);
});
// Handle process termination
process.on('SIGINT', () => {
    console.error('Shutting down Eventbrite MCP server...');
    process.exit(0);
});
process.on('SIGTERM', () => {
    console.error('Shutting down Eventbrite MCP server...');
    process.exit(0);
});
