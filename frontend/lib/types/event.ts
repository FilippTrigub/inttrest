import { ObjectId } from 'mongodb';

// Simple event interface with only required fields typed
export interface Event {
  _id?: ObjectId;
  geometry: {
    longitude: number;
    latitude: number;
  };
  datetime: Date;
  title: string;
  // All other fields are dynamic and untyped
  [key: string]: any;
}

// Input type for creating events
export interface CreateEventInput {
  geometry: {
    longitude: number;
    latitude: number;
  };
  datetime: string | Date;
  title: string;
  [key: string]: any;
}

// Simple filters
export interface EventFilters {
  limit?: number;
  skip?: number;
}