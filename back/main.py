from RouteOptimizer import RouteOptimizer
from LocationObject import LocationObject
import numpy
import LocationParser

depot = LocationObject("Gdynia", "81-364", "Władysława IV", "24", "09:00:00", "22:00:00")

routeOptimizer = RouteOptimizer(LocationParser.parse("/smallData.json"), depot)

print(routeOptimizer.create_data_model())
routeOptimizer.solve()