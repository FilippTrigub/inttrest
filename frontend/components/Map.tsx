'use client';

import React, { useState } from 'react';
import Map from 'react-map-gl';

const MapComponent = ({ accessToken }: { accessToken: string }) => {
  const [viewState, setViewState] = useState({
    longitude: 2.3522,
    latitude: 48.8566,
    zoom: 10
  });

  return (
    <Map
      mapboxAccessToken={accessToken}
      initialViewState={viewState}
      style={{ width: '100%', height: '100%' }}
      mapStyle="mapbox://styles/mapbox/streets-v11"
      onMove={evt => setViewState(evt.viewState)}
    />
  );
};

export default MapComponent;