import { useRef, useState } from "react";
import classes from './RouteCreator.module.css';
import LocationsList from "../LocationsList/LocationsList";

const RouteCreator = () => {

    const [locations, setLocations] = useState([]);
    const locationInput = useRef();

    const locationAddHandler = async () => {
        const request = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(locationInput.current.value)}&key=${process.env.REACT_APP_GOOGLE_MAPS_KEY}`);
        if (locationInput.current.value.trim() !== "" &&
            !locations.map(point => point.location.toLowerCase()).includes(locationInput.current.value.toLowerCase()) &&
            request.ok) {
            setLocations(prevState => [...prevState, { location: locationInput.current.value, stopover: true }]);
        } else {
            alert('wrong data');
        }
    };

    const submitHandler = async () => {
        //TODO send data to the backend
    }

    return (
        <div>
            <input className={`${classes['location-input']}`} type="text" placeholder="Enter Location Here" ref={locationInput} />
            <button className={`${classes['add-button']}`} onClick={async () => await locationAddHandler()}>Add</button>
            <LocationsList locations={locations} listType="1" />
            <button onClick={async () => await submitHandler()} className={`${classes['submit-button']}`}>Send</button>
        </div>
    );
}

export default RouteCreator;