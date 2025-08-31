'use client';

import MapComponent from '@/components/Map';
import ChatComponent from '@/components/Chat';
import { useEvents } from '@/hooks/useEvents';

export default function Home() {
  const { events, fetchEvents } = useEvents();

  return (
    <div className="h-screen w-screen grid grid-cols-1 md:grid-cols-3">
      <div className="md:col-span-1 bg-gray-800 flex flex-col h-screen">
        <ChatComponent onStreamingFinished={fetchEvents} />
      </div>
      <div className="md:col-span-2 bg-gray-700 h-full w-full">
        <MapComponent 
          accessToken={process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || ''} 
          events={events}
        />
      </div>
    </div>
  );
}