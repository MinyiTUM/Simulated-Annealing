####
#   Objectives Class with performance functions
#   E.g. number of vehicles of different types, route distance, cost function
import string
from typing import List
from Construction import *


class Instance:
    def __init__(self, id: List[str], demand_kg: List[int], demand_size: List[int], duration_S: string,
                 from_id: List[str], to_id: List[str], distance_total: List[float], distance_inside: List[float],
                 distance_outside: List[float], duration_T: string):
        self.id = id
        """id of nodes"""
        self.demand_kg = demand_kg
        """demand in kg per node"""
        self.demand_size = demand_size
        """demand in size per node"""
        self.duration_S = duration_S
        """service duration per node"""
        self.from_id = from_id
        """from_id of node"""
        self.to_id = to_id
        """to_id of node"""
        self.distance_total = distance_total
        """total distance per node"""
        self.distance_inside = distance_inside
        """inside distance per node"""
        self.distance_outside = distance_outside
        """outside distance per node"""
        self.duration_T = duration_T
        """transportation duration per node"""


vehicles = {'name': ["ICEV_I", "ICEV_II", "ICEV_III", "BEV_IV", "BEV_V", "BEV_VI", "LEFV (VII)"],
            'payload': [2800, 883, 670, 2800, 905, 720, 100],
            'surface_area': [14.82, 4.37, 2.21, 9.80, 5.45, 3.58, 0.38],
            'volume_area': [34800, 5800, 3200, 21560, 7670, 4270, 200],
            'acquisition_cost': [50.00, 29.15, 20.62, 47.52, 45.45, 35.95, 5.30],
            'resell_value': [25.00, 14.58, 10.31, 21.38, 20.45, 16.18, 2.39],
            'reach': [685.7143, 875, 932.2034, 79.7101, 205.0231, 118.9768, 200],
            'maintenance_cost': [0.0590, 0.0590, 0.0590, 0.0490, 0.0490, 0.0490, 0.0490],
            'area_restriction': [True, True, True, False, False, False, False],
            'heavy_truck': [True, False, False, True, False, False, False],
            'consumption_cost': [0.1750, 0.0800, 0.0590, 0.8280, 0.1951, 0.1681, 0],
            'driving_cost_Paris': [0.252, 0.1152, 0.08496, 0.11592, 0.027314, 0.027314, 0],
            'driving_cost_Shanghai': [0.13475, 0.0616, 0.04543, 0.0828, 0.01951, 0.01951, 0],
            'driving_cost_New_York': [0.11025, 0.0504, 0.03717, 0.09108, 0.021461, 0.018491, 0]}

semi_truck_driver_costs = {'Paris': 0.383838384, 'Shanghai': 0.477253929, 'New_York': 0.116331096}
heavy_truck_driver_costs = {'Paris': 0.398530762, 'Shanghai': 0.445822994, 'New_York': 0.133482476}
shift_duration = {'Paris': 435.6, 'Shanghai': 536.4, 'New_York': 483.6}

Route = List[int]  # first element is vehicle type
Solution = List[Route]

def inner_distance_fromId_toId(instance: Instance, fromId_index: int, toId_index: int) -> float:
    fromId = instance.from_id
    toId = instance.to_id
    dis_inside = instance.distance_inside

    if fromId_index == 0 and toId_index == 0:  # from depot to depot
        return 0.0
    elif toId_index == 0 and fromId_index != 0:  # from customer to depot
        from_cus = "C" + str(fromId_index)
        to_cus = "D" + str(toId_index)
    elif fromId_index == 0 and toId_index != 0:  # from depot to customer
        from_cus = "D" + str(fromId_index)
        to_cus = "C" + str(toId_index)
    else:  # from customer to customer
        from_cus = "C" + str(fromId_index)
        to_cus = "C" + str(toId_index)

    targeted_counter_fromId = 0
    targeted_counter_toId = 0
    # counter indexes for searching the position of total distance

    for i in fromId:
        if i == from_cus:
            for j in toId:
                if j == to_cus:
                    return dis_inside[targeted_counter_fromId + targeted_counter_toId]
                targeted_counter_toId += 1
        targeted_counter_fromId += 1

    # if the inputs are abnormal, return default 0.0
    return 0.0


def transportation_duration_fromId_toId(instance: Instance, fromId_index: int, toId_index: int) -> string:
    fromId = instance.from_id
    toId = instance.to_id
    transportation_duration = instance.duration_T

    if fromId_index == 0 and toId_index == 0:  # from depot to depot
        return 0.0
    elif toId_index == 0 and fromId_index != 0:  # from customer to depot
        from_cus = "C" + str(fromId_index)
        to_cus = "D" + str(toId_index)
    elif fromId_index == 0 and toId_index != 0:  # from depot to customer
        from_cus = "D" + str(fromId_index)
        to_cus = "C" + str(toId_index)
    else:  # from customer to customer
        from_cus = "C" + str(fromId_index)
        to_cus = "C" + str(toId_index)

    targeted_counter_fromId = 0
    targeted_counter_toId = 0
    # counter indexes for searching the position of total distance

    for i in fromId:
        if i == from_cus:
            for j in toId:
                if j == to_cus:
                    return transportation_duration[targeted_counter_fromId + targeted_counter_toId]
                targeted_counter_toId += 1
        targeted_counter_fromId += 1

    # if the inputs are abnormal, return default 0.0
    return 0.0


def calculate_route_demand_kg(route: Route, instance: Instance) -> int:
    route_demand_kg = 0
    from Construction import create_unserved_cus
    if len(route) < 4:
        return 0
    else:
        for i in range(1, len(route) - 1):
            if route[i] != 0:
             route_demand_kg = route_demand_kg + int(instance.demand_kg[create_unserved_cus(instance).index(route[i])+1])
    return route_demand_kg


def calculate_route_demand_size(route: Route, instance: Instance) -> int:
    route_demand_size = 0
    from Construction import create_unserved_cus
    if len(route) < 4:
        return 0
    else:
        for i in range(1, len(route) - 1):
            if route[i]!=0:
             route_demand_size = route_demand_size + int(instance.demand_size[create_unserved_cus(instance).index(route[i])+1])
    return route_demand_size


def calculate_route_distance(route: Route, instance: Instance) -> float:
    route_distance: float = 0.0
    from Construction import distance_fromId_toId
    if len(route) < 4:
        return 0.0
    else:
        for i in range(1, len(route) - 1):
            route_distance = route_distance + float(distance_fromId_toId(instance, route[i], route[i + 1]))
    return route_distance


def calculate_route_inner_distance(route: Route, instance: Instance) -> float:
    route_distance: float = 0.0
    if len(route) < 4:
        return 0.0
    else:
        for i in range(1, len(route) - 1):
            route_distance = route_distance + float(inner_distance_fromId_toId(instance, route[i], route[i + 1]))
    return route_distance


def calculate_total_number_of_vehicles(solution: Solution) -> int:
    return len(solution)


def calculate_solution_distance(solution: Solution, instance: Instance) -> float:
    solution_distance: float = 0.0
    for route in range(0, len(solution)):
        solution_distance += calculate_route_distance(solution[route], instance)
    return solution_distance


def calculate_total_minutes_in_duration(duration: string) -> float:
    number_of_minutes: float = 0.0
    (h, m, s) = duration.split(':')
    number_of_minutes = float(h) * 60 + float(m) + float(s) / 60
    return number_of_minutes


def calculate_transportation_and_service_time(route: Route, instance: Instance) -> float:
    duration: float = 0.0
    from Construction import create_unserved_cus
    if len(route) < 4:
        duration = 0.0
    else:
        for i in range(1, len(route) - 1):
            if route[i]!=0:
                duration += calculate_total_minutes_in_duration(
                    transportation_duration_fromId_toId(instance, route[i], route[i + 1])) \
                        + calculate_total_minutes_in_duration(instance.duration_S[create_unserved_cus(instance).index(route[i])+1])
            else:
                duration += calculate_total_minutes_in_duration(
                    transportation_duration_fromId_toId(instance, route[i], route[i + 1]))
    return duration


def calculate_number_of_vehicles_of_type_k(solution: Solution, vehicle_type_k: int) -> int:
    number_of_vehicles_of_type_k: int = 0
    for route in solution:
        if route[0] == vehicle_type_k:
            number_of_vehicles_of_type_k += 1
    return number_of_vehicles_of_type_k


# total number of vehicles of each type
def calculate_number_of_vehicles_of_each_type(solution: Solution) -> List:
    total_number_of_vehicles_of_each_type = [calculate_number_of_vehicles_of_type_k(solution, vehicle_type_k)
                                             for vehicle_type_k in range(1, 8)]
    return total_number_of_vehicles_of_each_type


# fuel, electricity and maintenance costs
def calculate_operational_costs(solution: Solution, city: string, instance: Instance) -> float:
    operational_costs = 0.0
    maintenance_cost_list = vehicles['maintenance_cost']
    driving_cost_Paris_list = vehicles['driving_cost_Paris']
    driving_cost_Shanghai_list = vehicles['driving_cost_Shanghai']
    driving_cost_New_York_list = vehicles['driving_cost_New_York']
    for route in solution:
        if city == "Paris":
            if route[0] == 4 or route[0] == 5 or route[0] == 6 or route[0] == 7:
                operational_costs += 0.95 * ((float(maintenance_cost_list[route[0] - 1]) + float
                (driving_cost_Paris_list[route[0] - 1])) * calculate_route_distance(route, instance))
            else:
                operational_costs += (float(maintenance_cost_list[route[0] - 1]) + float(
                    driving_cost_Paris_list[route[0] - 1])) * calculate_route_distance(route, instance)
        elif city == "Shanghai":
            operational_costs += (float(maintenance_cost_list[route[0] - 1]) + float(
                driving_cost_Shanghai_list[route[0] - 1])) * calculate_route_distance(route, instance)
        else:
            operational_costs += (float(maintenance_cost_list[route[0] - 1]) + float(
                driving_cost_New_York_list[route[0] - 1])) * calculate_route_distance(route, instance)
    return operational_costs


# inner city tolling costs
def calculate_inner_city_tolling_costs(solution: Solution, city_toll: float, instance: Instance) -> float:
    inner_city_tolling_costs = 0.0
    for route in solution:
        if route[0] == 1 or route[0] == 2 or route[0] == 3:
            inner_city_tolling_costs += float(calculate_route_inner_distance(route, instance)) * city_toll
    return inner_city_tolling_costs


# wage costs for travel and service time of drivers
def calculate_wage_costs(solution: Solution, city: string, instance: Instance) -> float:
    total_wage_costs = 0.0
    driver_wage = 0.0
    for route in solution:
        if route[0] == 1 or route[0] == 4:  # heavy trucks are vehicles 1 and 4
            driver_wage = float(heavy_truck_driver_costs[city])
        else:
            driver_wage = float(semi_truck_driver_costs[city])
        total_wage_costs += driver_wage * calculate_transportation_and_service_time(route, instance)
    return total_wage_costs


# daily utility costs for the vehicles used
def total_daily_utility_costs_of_vehicles(solution: Solution, city: string, instance: Instance) -> float:
    total_daily_utility_costs_of_vehicles: float = 0.0
    acquisition_cost_list = vehicles['acquisition_cost']
    resell_value_list = vehicles['resell_value']
    if city == "Paris":
        for i in range(1, 4):
            total_daily_utility_costs_of_vehicles += calculate_number_of_vehicles_of_type_k(solution, i) * (
                        float(acquisition_cost_list[i - 1]) - float(resell_value_list[i - 1]))
        for i in range(4, 8):
            total_daily_utility_costs_of_vehicles += calculate_number_of_vehicles_of_type_k(solution, i) * 0.95 * (
                        float(acquisition_cost_list[i - 1]) - float(resell_value_list[i - 1]))
    else:
        for i in range(1, 8):
            total_daily_utility_costs_of_vehicles += calculate_number_of_vehicles_of_type_k(solution, i) * \
                                                     (float(acquisition_cost_list[i - 1]) - float(
                                                         resell_value_list[i - 1]))
    return total_daily_utility_costs_of_vehicles


def total_cost(solution: Solution, instance: Instance, city: string, city_toll: float) -> float:
    total_costs: float = 0.0
    total_costs = calculate_operational_costs(solution, city, instance) \
                  + calculate_inner_city_tolling_costs(solution, city_toll, instance) \
                  + calculate_wage_costs(solution, city, instance) \
                  + total_daily_utility_costs_of_vehicles(solution, city, instance)
    return total_costs

