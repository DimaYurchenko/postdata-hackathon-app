
import React, { useEffect, useState } from 'react';
import GoogleMapReact from 'google-map-react';
import LocationsList from './LocationsList/LocationsList';
import LandMark from './LandMark';

const SimpleMap = (props) => {
  //example of backend response 
  const [points, setPoints] = useState(
    [{ location: '81-532, Witolda 17, Gdynia', stopover: true },
    { location: '81-532, Witolda 39A, Gdynia', stopover: true },
    { location: '81-532, Wielkoplska 260, Gdynia', stopover: true },
    { location: '81-587, Korzenna 16A, Gdynia', stopover: true },
    { location: '81-578, Wiczlinska 4, Gdynia', stopover: true },
    { location: '81-356, Starowiejska 40C, Gdynia', stopover: true },
    { location: '81-366, 10 Lutego 7, Gdynia', stopover: true },
    { location: '81-395, A. Abrahama 46 A-B, Gdynia', stopover: true },
    { location: '81-389, Świętojańska 75, Gdynia', stopover: true },
    { location: '81-389, Swietojanska 75 , Gdynia', stopover: true },
    { location: '81-377, Ignacego Krasickiego 45, Gdynia', stopover: true },
    { location: '81-377, Necla 5, Gdynia', stopover: true },
    { location: '81-415, B. Chłopskich 24, Gdynia', stopover: true },
    { location: '81-537, Łużycka 3, Gdynia', stopover: true },
    { location: '81-537, Luzycka 3A, Gdynia', stopover: true },
    { location: '81-509, plac Górnośląski 4A, Gdynia', stopover: true },
    { location: '81-540, aleja Zwycięstwa 238, Gdynia', stopover: true }]
  );

  //uncomment during loading data from backend
  //fill out REACT_APP_API variable in .env
  //check latest .env file in discrord
  // useEffect(() => {
  //   let fetchData = async () => {
  //     try {
  //       const requestData = await (await fetch(process.env.REACT_APP_API + '/defaultdata')).json().map(point => ({...point, stopover: true}));
  //       setPoints(requestData);
  //     } catch (error) {
  //       console.log('fetching error ocured', error);
  //     }
  //   }

  //   fetchData();
  // }, []);

  const apiIsLoaded = (map, maps) => {
    const directionsService = new window.google.maps.DirectionsService();
    const directionsRenderer = new window.google.maps.DirectionsRenderer();

    directionsRenderer.setMap(map);

    if (points.length <= 26) {
      directionsService.route(
        {
          origin: points[0].location,
          destination: points[0].location,
          waypoints: points.length > 2 ? points.slice(1, points.length) : [],
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
    }

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
        {points.length >= 26 &&
          points.map((point, index) => <LandMark key={index} text={index + 1} long={point.long} lat={point.lat} />)
        }
      </div>
      <LocationsList locations={[...points.slice(), points[0]]} listType={points.length >= 26 ? '1' : 'A'} />
    </div>
  );
}


export default SimpleMap;