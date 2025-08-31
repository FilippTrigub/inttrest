"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.listEvents = listEvents;
const eventbriteClient_1 = __importDefault(require("../../api/eventbriteClient"));
/**
 * List events with filtering options
 */
async function listEvents(params = {}) {
    try {
        // Map MCP tool parameters to Eventbrite API parameters
        const apiParams = {
            status: params.status || '',
            start_date: params.start_date || '',
            end_date: params.end_date || '',
            page: params.page || 1,
            page_size: params.page_size || 50
        };
        // Filter out empty values
        Object.keys(apiParams).forEach(key => {
            if (apiParams[key] === '') {
                delete apiParams[key];
            }
        });
        // Log the parameters we're using
        console.error('MCP listEvents parameters:', JSON.stringify(params, null, 2));
        console.error('API parameters after filtering:', JSON.stringify(apiParams, null, 2));
        // Call Eventbrite API using the organization events endpoint for better filtering
        const response = await eventbriteClient_1.default.searchEvents(apiParams);
        // Transform response to a more usable format for the MCP client
        const events = response.events.map((event) => ({
            id: event.id,
            name: event.name.text,
            description: event.description?.text || '',
            url: event.url,
            start: event.start.utc,
            end: event.end.utc,
            status: event.status,
            currency: event.currency,
            online_event: event.online_event,
            venue_id: event.venue_id,
            organizer_id: event.organizer_id,
            created: event.created,
            changed: event.changed,
            capacity: event.capacity,
            is_free: event.is_free
        }));
        return {
            events,
            pagination: response.pagination
        };
    }
    catch (error) {
        console.error('Error in listEvents tool:', error);
        throw new Error(`Failed to list events: ${error.message}`);
    }
}
