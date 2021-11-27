
import React from 'react';
import GoogleMapReact from 'google-map-react';
import LocationsList from './LocationsList/LocationsList';

const SimpleMap = (props) => {
  const points = [
    { location: '81-532, Witolda 39A, Gdynia', stopover: true },
    { location: '81-587, Korzenna 16A, Gdynia', stopover: true },
    { location: '81-578, Wiczlinska 4, Gdynia', stopover: true },
    { location: '81-356, Starowiejska 40C, Gdynia', stopover: true },
    { location: '81-366, 10 Lutego 7, Gdynia', stopover: true },
    { location: '81-532, Wielkoplska 260, Gdynia', stopover: true },
  ];
    
  const apiIsLoaded = (map, maps) => {
    const directionsService = new window.google.maps.DirectionsService();
    const directionsRenderer = new window.google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    directionsService.route(
      {
        origin: points[0].location,
        destination: points[points.length - 1].location,
        waypoints: points.length > 2 ? points.slice(1, -1) : [],
        travelMode: window.google.maps.TravelMode.DRIVING
      },
      (result, status) => {
        if (status === window.google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);
        } else {
          console.error(`error fetching directions ${result}`);
        }
      }
    );
  };
  return (
    <div>
      <div style={{ height: '600px', width: '98%', margin: 'auto' }}>
        <GoogleMapReact
          bootstrapURLKeys={{
            key: process.env.REACT_APP_GOOGLE_MAPS_KEY
          }}
          defaultCenter={{ lat: 52, lng: 20 }}
          defaultZoom={10}
          yesIWantToUseGoogleMapApiInternals
          onGoogleApiLoaded={({ map, maps }) => apiIsLoaded(map, maps)}
        />
      </div>
      <LocationsList locations={points} />
    </div>
  );
}


export default SimpleMap;