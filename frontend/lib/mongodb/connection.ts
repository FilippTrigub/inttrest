import { MongoClient, Db, MongoClientOptions } from 'mongodb';

class MongoConnection {
  private static instance: MongoConnection;
  private client: MongoClient | null = null;
  private db: Db | null = null;

  private constructor() {}

  public static getInstance(): MongoConnection {
    if (!MongoConnection.instance) {
      MongoConnection.instance = new MongoConnection();
    }
    return MongoConnection.instance;
  }

  public async connect(): Promise<void> {
    if (this.client && this.db) return;

    const uri = process.env.MONGODB_URI;
    if (!uri) {
      throw new Error('MONGODB_URI environment variable is required');
    }

    const options: MongoClientOptions = {
      maxPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
    };

    this.client = new MongoClient(uri, options);
    await this.client.connect();
    
    const dbName = process.env.MONGODB_DB_NAME || 'events_db';
    this.db = this.client.db(dbName);

    // Simple validation - only check required fields
    await this.setupCollection();
  }

  private async setupCollection(): Promise<void> {
    if (!this.db) return;

    try {
      await this.db.createCollection('events', {
        validator: {
          $jsonSchema: {
            bsonType: 'object',
            required: ['geometry', 'datetime', 'title'],
            properties: {
              geometry: {
                bsonType: 'object',
                required: ['longitude', 'latitude'],
                properties: {
                  longitude: { bsonType: 'number', minimum: -180, maximum: 180 },
                  latitude: { bsonType: 'number', minimum: -90, maximum: 90 }
                }
              },
              datetime: { bsonType: 'date' },
              title: { bsonType: 'string', minLength: 1 }
            }
          }
        }
      });

      // Basic indexes
      await this.db.collection('events').createIndexes([
        { key: { datetime: 1 } },
        { key: { 'geometry.longitude': 1, 'geometry.latitude': 1 } }
      ]);
    } catch (error: any) {
      // Ignore if collection already exists
      if (error.code !== 48) {
        console.warn('Collection setup warning:', error.message);
      }
    }
  }

  public getDb(): Db {
    if (!this.db) {
      throw new Error('Database not connected');
    }
    return this.db;
  }

  public async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.close();
      this.client = null;
      this.db = null;
    }
  }
}

export const mongoConnection = MongoConnection.getInstance();

export const getDatabase = async (): Promise<Db> => {
  await mongoConnection.connect();
  return mongoConnection.getDb();
};