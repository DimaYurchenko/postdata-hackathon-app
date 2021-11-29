from typing import Dict, List
from LocationObject import LocationObject
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import googlemaps
import numpy as np
import os                                                                                                                                                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from time import strftime
from time import gmtime



class RouteOptimizer:

    def __init__(self, locations: List[LocationObject], depot: LocationObject = None) -> None:
        if not depot == None:
            locations.insert(0, depot)
            self.locations = locations
        else:
            self.locations = locations

        self.timeMatrix = None
 

    
    def buildTimeMatrix(self):
        def build(locations: List[LocationObject]):
            dimensions = len(locations)
            timeMatrix = np.zeros((dimensions, dimensions), int)

            load_dotenv(Path(".env"))
            apiKey = os.getenv("MAPS_API_KEY")

            gmaps = googlemaps.Client(key=apiKey)  
            for i in range(0, dimensions):
                for j in range(i+1, dimensions):

                    apiResponse = gmaps.distance_matrix(origins=locations[i].fullAdress, 
                        destinations = locations[j].fullAdress, mode="driving")

                    timeBetweenLocations: int = apiResponse["rows"][0]["elements"][0]["duration"]["value"]
                    timeMatrix[i][j] = timeBetweenLocations
                    timeMatrix[j][i] = timeBetweenLocations

            return timeMatrix.tolist()

        self.timeMatrix = build(self.locations)

        return self.timeMatrix

    def createDataModel(self):
        data = {}
        if self.timeMatrix == None:
            self.buildTimeMatrix()

        data['time_matrix'] = self.timeMatrix

        timeWindows = []

        for location in self.locations:
            timeWindows.append((int(location.getOpenHours() * 3600), int(location.getCloseHours() * 3600)))

        data['time_windows'] = timeWindows

        data['num_vehicles'] = 1
        data['depot'] = 0

        self.dataModel = data
        return data           
        
    def printSolution(self):

        print(f'Objective: {self.solution.ObjectiveValue()}')
        time_dimension = self.routing.GetDimensionOrDie('Time')
        total_time = 0
        for vehicle_id in range(self.data['num_vehicles']):
            index = self.routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            while not self.routing.IsEnd(index):
                time_var = time_dimension.CumulVar(index)
                plan_output += '{0} Time({1},{2}) -> '.format(
                    self.manager.IndexToNode(index), strftime("%H:%M:%S", gmtime(self.solution.Min(time_var))),
                    strftime("%H:%M:%S", gmtime(self.solution.Max(time_var))))
                index = self.solution.Value(self.routing.NextVar(index))
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2})\n'.format(self.manager.IndexToNode(index),
                                                        strftime("%H:%M:%S", gmtime(self.solution.Min(time_var))),
                                                        strftime("%H:%M:%S", gmtime(self.solution.Max(time_var))))

            route_time = self.solution.Min(time_var) - self.solution.Min(time_dimension.CumulVar(0))
            plan_output += f'Time of the route: {route_time}sec\n'
            print(plan_output)
            total_time += route_time
        print('Total time of all routes: {}sec'.format(total_time))

    def writeSolution(self, filePath: str="solution.txt"):
        with open(filePath, 'w') as file:
            file.write(f'Objective: {self.solution.ObjectiveValue()}')
            time_dimension = self.routing.GetDimensionOrDie('Time')
            total_time = 0
            for vehicle_id in range(self.data['num_vehicles']):
                index = self.routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                while not self.routing.IsEnd(index):
                    time_var = time_dimension.CumulVar(index)
                    plan_output += '{0} Time({1},{2}) -> '.format(
                        self.manager.IndexToNode(index), self.solution.Min(time_var),
                        self.solution.Max(time_var))
                    index = self.solution.Value(self.routing.NextVar(index))
                time_var = time_dimension.CumulVar(index)
                plan_output += '{0} Time({1},{2})\n'.format(self.manager.IndexToNode(index),
                                                            self.solution.Min(time_var),
                                                            self.solution.Max(time_var))
                plan_output += 'Time of the route: {}sec\n'.format(
                    self.solution.Min(time_var))
                file.write(plan_output)
                total_time += self.solution.Min(time_var)
            file.write('Total time of all routes: {}sec'.format(total_time))
            




    def solve(self):
        # Instantiate the data problem.
        data = self.createDataModel()
        print("data model created")

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                            data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.
        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            # Convert from routing variable Index to time matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['time_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(time_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Time Windows constraint.
        time = 'Time'
        routing.AddDimension(
            transit_callback_index,
            20000,  # allow waiting time
            86400,  # maximum time per vehicle
            False,  # Don't force start cumul to zero.
            time)
        time_dimension = routing.GetDimensionOrDie(time)
        # Add time window constraints for each location except depot.
        for location_idx, time_window in enumerate(data['time_windows']):
            if location_idx == data['depot']:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        # Add time window constraints for each vehicle start node.
        depot_idx = data['depot']
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(
                data['time_windows'][depot_idx][0],
                data['time_windows'][depot_idx][1])

        # Instantiate route start and end times to produce feasible times.
        for i in range(data['num_vehicles']):
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.Start(i)))
            routing.AddVariableMinimizedByFinalizer(
                time_dimension.CumulVar(routing.End(i)))

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        # print(solution)
        # Print solution on console.
        if solution:
            self.solution = solution
            self.manager = manager
            self.routing = routing
            self.data = data
            self.printSolution()
        
