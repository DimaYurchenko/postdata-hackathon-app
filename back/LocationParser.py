import json
from typing import List
from LocationObject import LocationObject

def parse(file_path: str) -> List[LocationObject]:
    with open(file_path, "r") as file:
        data = json.loads(file.read().replace("\n", ""))

        locations: List[LocationObject] = []

        for object in data:
            city = object["City"]
            code = object["PostalCode"]
            street = object["Street"]

            streetNum = str(object["StreetNumber"])
            openTime = object["OpenTime"]
            closeTime = object["CloseTime"]

            location = LocationObject(city, code, street, streetNum, openTime, closeTime)
            locations.append(location)

        uniqueLocations = []
        for i in locations:
            if i not in uniqueLocations:
                uniqueLocations.append(i)


        return uniqueLocations

# add geocoding for each location

