import { v4 as uuidv4} from 'uuid';

const LocationsList = ({ locations = [], listType = 'A' }) => {

  return (
    <ol type={listType}>
      {
        locations.map((point) => {
          return <li key={uuidv4()} >{point.location}</li>
        })
      }
    </ol>
  )

}
export default LocationsList;