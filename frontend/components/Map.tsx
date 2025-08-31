'use client';

import React, { useState } from 'react';
import Map, { Source } from 'react-map-gl';

const MapComponent = ({ accessToken }: { accessToken: string }) => {
  const [viewState, setViewState] = useState({
    longitude: 2.3522,
    latitude: 48.8566,
    zoom: 15,
    pitch: 60,
    bearing: 0
  });

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