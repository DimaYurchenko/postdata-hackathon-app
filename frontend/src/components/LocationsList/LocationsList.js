const LocationsList = ({ locations = [], listType = 'A' }) => {

  return (
    <ol type={listType}>
      {
        locations.map((point, index) => {
          return <li key={index} >{point.location}</li>
        })
      }
    </ol>
  )

}
export default LocationsList;