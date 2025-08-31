'use client';

import React, { useState, useEffect } from 'react';
import Map, { Source } from 'react-map-gl';
import { Event } from '@/lib/types/event';

interface MapComponentProps {
  accessToken: string;
  events?: Event[];
}

const MapComponent = ({ accessToken, events = [] }: MapComponentProps) => {
  const [viewState, setViewState] = useState({
    longitude: 2.3522,
    latitude: 48.8566,
    zoom: 15,
    pitch: 60,
    bearing: 0
  });

  // Update view state when events change
  useEffect(() => {
    if (events.length > 0) {
      // Calculate center point of all events
      const avgLongitude = events.reduce((sum, event) => sum + event.geometry.longitude, 0) / events.length;
      const avgLatitude = events.reduce((sum, event) => sum + event.geometry.latitude, 0) / events.length;
      
      // Calculate appropriate zoom level based on event spread
      const lngs = events.map(e => e.geometry.longitude);
      const lats = events.map(e => e.geometry.latitude);
      const maxLng = Math.max(...lngs);
      const minLng = Math.min(...lngs);
      const maxLat = Math.max(...lats);
      const minLat = Math.min(...lats);
      
      const lngSpread = maxLng - minLng;
      const latSpread = maxLat - minLat;
      const spread = Math.max(lngSpread, latSpread);
      
      // Simple zoom calculation - adjust as needed
      let zoom = 15;
      if (spread > 0.1) zoom = 10;
      else if (spread > 0.05) zoom = 12;
      else if (spread > 0.01) zoom = 14;
      
      setViewState(prev => ({
        ...prev,
        longitude: avgLongitude,
        latitude: avgLatitude,
        zoom,
      }));
    }
  }, [events]);

  return (
    <Map
      mapboxAccessToken={accessToken}
      initialViewState={viewState}
      style={{ width: '100%', height: '100%' }}
      mapStyle="mapbox://styles/mapbox/standard"
      antialias={true}
      terrain={{ source: 'mapbox-dem', exaggeration: 1.5 }}
      onMove={evt => setViewState(evt.viewState)}
    >
      <Source
        id="mapbox-dem"
        type="raster-dem"
        url="mapbox://mapbox.mapbox-terrain-dem-v1"
        tileSize={512}
        maxzoom={14}
      />
    </Map>
  );
};

export default MapComponent;