import { Collection, ObjectId } from 'mongodb';
import { getDatabase } from '../mongodb/connection';
import { Event, CreateEventInput, EventFilters } from '../types/event';

export class EventsRepository {
  private static instance: EventsRepository;
  private collection: Collection<Event> | null = null;

  private constructor() {}

  public static getInstance(): EventsRepository {
    if (!EventsRepository.instance) {
      EventsRepository.instance = new EventsRepository();
    }
    return EventsRepository.instance;
  }

  private async getCollection(): Promise<Collection<Event>> {
    if (!this.collection) {
      const db = await getDatabase();
      this.collection = db.collection<Event>('events');
    }
    return this.collection;
  }

  // Create event
  async create(eventData: CreateEventInput): Promise<Event> {
    const collection = await this.getCollection();
    
    const event = {
      ...eventData,
      datetime: new Date(eventData.datetime),
    };

    const result = await collection.insertOne(event);
    return { _id: result.insertedId, ...event };
  }

  // Find by ID
  async findById(id: string): Promise<Event | null> {
    const collection = await this.getCollection();
    return await collection.findOne({ _id: new ObjectId(id) });
  }

  // Find all with pagination
  async findMany(filters: EventFilters = {}): Promise<Event[]> {
    const collection = await this.getCollection();
    const { limit = 50, skip = 0 } = filters;
    
    return await collection
      .find({})
      .sort({ datetime: 1 })
      .skip(skip)
      .limit(limit)
      .toArray();
  }

  // Update event
  async update(id: string, updateData: Partial<CreateEventInput>): Promise<Event | null> {
    const collection = await this.getCollection();
    
    const processedData = { ...updateData };
    if (updateData.datetime) {
      processedData.datetime = new Date(updateData.datetime);
    }

    await collection.updateOne(
      { _id: new ObjectId(id) },
      { $set: processedData }
    );

    return await this.findById(id);
  }

  // Delete event
  async delete(id: string): Promise<boolean> {
    const collection = await this.getCollection();
    const result = await collection.deleteOne({ _id: new ObjectId(id) });
    return result.deletedCount > 0;
  }
}

export const eventsRepository = EventsRepository.getInstance();