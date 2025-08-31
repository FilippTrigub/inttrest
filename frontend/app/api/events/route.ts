import { NextRequest, NextResponse } from 'next/server';
import { eventsRepository } from '@/lib/repositories/events.repository';
import { validateCreateEvent } from '@/lib/validation/event.validation';

// GET /api/events
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get('limit') ? parseInt(searchParams.get('limit')!) : undefined;
    const skip = searchParams.get('skip') ? parseInt(searchParams.get('skip')!) : undefined;

    const events = await eventsRepository.findMany({ limit, skip });
    
    return NextResponse.json({ events });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

// POST /api/events
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = validateCreateEvent(body);
    const event = await eventsRepository.create(validatedData);
    
    return NextResponse.json({ event }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }
}