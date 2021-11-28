import time

class LocationObject:

    def __init__(self, city: str, postalCode: str, street: str, 
        streetNum: str, openTime: str, closeTime: str ):

        self.city = city
        self.postalCode = postalCode
        self.street = street
        self.streetNum = streetNum

        self.fullAdress: str = f'{postalCode}, {street} {streetNum}, {city}'

        timestamp = time.strftime('%H:%M:%S')
        self.openTime: time = openTime.format(timestamp)
        self.closeTime: time = closeTime.format(timestamp)

    def __key(self):
        return (self.fullAdress)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, LocationObject):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self) -> str:
        return '{' + f'{self.fullAdress}, {self.openTime}, {self.closeTime}' + '}'

    def __repr__(self):
        return self.__str__()

    def getOpenHours(self):
        return int(self.openTime.split(":")[0])

    def getCloseHours(self):
        return int(self.closeTime.split(":")[0])


        