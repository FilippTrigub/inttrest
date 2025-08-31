import { z } from 'zod';

// Simple validation for required fields only
export const CreateEventSchema = z.object({
  geometry: z.object({
    longitude: z.number().min(-180).max(180),
    latitude: z.number().min(-90).max(90),
  }),
  datetime: z.string().or(z.date()).transform((val) => new Date(val)),
  title: z.string().min(1, 'Title is required'),
}).passthrough(); // Allow additional fields

export const UpdateEventSchema = CreateEventSchema.partial().passthrough();

export const ObjectIdSchema = z.string().regex(/^[0-9a-fA-F]{24}$/, 'Invalid ID');

// Simple validation functions
export function validateCreateEvent(data: unknown) {
  return CreateEventSchema.parse(data);
}

export function validateUpdateEvent(data: unknown) {
  return UpdateEventSchema.parse(data);
}

export function validateObjectId(id: unknown) {
  return ObjectIdSchema.parse(id);
}