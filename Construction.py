###
#   Create complete solution for the CVRP
#   Include heuristics and metaheuristics methods

#   Create complete solution for the CVRP
#   Include heuristics and metaheuristics methods

from typing import List, Dict
from Objectives import Instance, Solution,Route
from Objectives import *
from copy import deepcopy

import math
import re
import random
import sys


random.seed(42)  # set random seed


def create_solution_simple_distance(ordered_customers: list[int], instance: Instance, vehicle_capacity_kg: int,
                                    vehicle_capacity_size: int, vehicle_max_reach: float, vehicle_type: int) -> Solution:
    """Assign c_i to route until the capacity in kg as well as
    capacity in size are not violated. if adding the customer would violate
    the constraint, close the route, create a new one, and add the customer there

    :param ordered_customers: ordered list of customers
    :param instance: Instance
    :return: Solution

    """
    #  not exceeded when closing the route and insert customers in between[vehicle_type, 0, i, 0]
    solution = list()
    open_route = [vehicle_type, 0]
    open_route_load_kg: int = 0
    open_route_load_size: int = 0
    open_route_distance: float = 0.0

    for i in ordered_customers:
        if int(open_route_load_kg) + int(instance.demand_kg[i]) > int(vehicle_capacity_kg) or int(
                open_route_load_size) + int(instance.demand_size[i]) > int(vehicle_capacity_size) or float(
                open_route_distance) + float(distance_fromId_toId(instance, open_route[-1], i)) > float(
                vehicle_max_reach):
            open_route.append(0)
            solution.append(open_route)
            open_route = [vehicle_type,0, i]
            open_route_load_kg = instance.demand_kg[i]
            open_route_load_size = instance.demand_size[i]
            open_route_distance = float(distance_fromId_toId(instance, open_route[-1], i))
            # instance.distance_total need to find correct from ID to ID

        else:
            open_route.append(i)
            open_route_load_kg = int(open_route_load_kg) + int(instance.demand_kg[i])
            open_route_load_size = int(open_route_load_size) + int(instance.demand_size[i])
            open_route_distance = float(open_route_distance) + float(distance_fromId_toId(instance, open_route[-2], i))

    open_route.append(0)
    solution.append(open_route)

    return solution


# Helping method to include the constraint of maximum reach
def distance_fromId_toId (instance: Instance, fromId_index: int, toId_index: int) -> float:
    # create a dataframe include fromId, toId and total distance between two IDs
    fromId = instance.from_id
    toId = instance.to_id
    dis_total = instance.distance_total

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
                    return dis_total[targeted_counter_fromId + targeted_counter_toId]
                targeted_counter_toId += 1
        targeted_counter_fromId += 1

    # if the inputs are abnormal, return default 0.0
    return 0.0

# helping function for nearest_neighbourhood function
def if_route_feasible_before_assignment(route: List, instance: Instance, vehicle: int, temp_unserved_cus: List) -> bool:
    payload=int(instance.demand_kg[temp_unserved_cus.index(route[-2])+1])
    demand_size=int(instance.demand_size[temp_unserved_cus.index(route[len(route) - 2])+1])
    distance= float(distance_fromId_toId(instance, 0, route[len(route) - 2]))+float(distance_fromId_toId(instance, route[len(route) - 2],0))
    #print("payload",payload)
    if payload < int(vehicles["payload"][vehicle]) and demand_size< int(vehicles[ "volume_area"][vehicle]) and distance<float(vehicles["reach"][vehicle]):
       return True

    return False

# helping function for nearest_neighbourhood function
# To find the next nearst customer
def find_neighbour(current_cus: int, unserved_cus: List, instance: Instance) -> int:
    min_distance = sys.float_info.max
    neighbour = -1
    for i in unserved_cus:
        if float(distance_fromId_toId(instance, current_cus, i)) <= float(min_distance) and i != current_cus:
            min_distance = distance_fromId_toId(instance, current_cus, i)
            neighbour = i
    return neighbour

# helping function for nearest_neighbourhood function
# To see if the current to be assigned customer is served or not
def if_served(unserved_cus: List, planned_served_cus: int) -> bool:
    for i in unserved_cus:
        if planned_served_cus == i:
            return False
    return True

def create_unserved_cus(instance)->list:
    unserved_cus = []  # a list to save all unserved customers
    for i in instance.id:
        num = ' '.join((re.findall(r'\d+', i)))
        num = int(num)
        if num==0:
            pass
        else:
            unserved_cus.append(num)
    return unserved_cus

# initial solution for simulated_annealing
def nearest_neighbourhood(instance: Instance, city: str) -> Solution:
    """Assign c_i to route until the capacity in kg as well as
        capacity in size, maximum reach and duration of workers are not violated. if adding the customer would violate
        the constraint, close the route, create a new one, and add the customer there. Vehicles are randomly assigned for
        each new route. customers are ordered based on the shortest distance of last chosen customer.

        :param instance: Instance
        :param city: str
        :return: Solution

        """
    unserved_cus = create_unserved_cus(instance)
    #print("unserved_cus", unserved_cus) # current customer to be assigned
    temp_unserved_cus=List.copy(unserved_cus)

    current_cus = unserved_cus[0]
    vehicle_type = [random.randrange(0, 7)]  # a list to save generated vehicle types
    counter_vehicle = 0  # counter of vehicle_type list
    open_route = [0, unserved_cus[0], 0]
    solution = list()

    open_route_load_kg = int(instance.demand_kg[temp_unserved_cus.index(current_cus)+1])
    open_route_load_size = int(instance.demand_size[temp_unserved_cus.index(current_cus)+1])
    open_route_distance = float(distance_fromId_toId(instance, 0, unserved_cus[0])) \
                          + float(distance_fromId_toId(instance, unserved_cus[0], 0))
    open_route_duration = calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, 0, unserved_cus[0])) \
                          + calculate_total_minutes_in_duration(instance.duration_S[unserved_cus[0]]) \
                          + calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, unserved_cus[0], 0))

    # the case that the initial customer can not be fit in one open route with random vehicle
    if if_route_feasible_before_assignment(open_route, instance, vehicle_type[counter_vehicle], temp_unserved_cus):
        unserved_cus.remove(current_cus)
        next_served_cus = find_neighbour(current_cus, unserved_cus, instance)
        current_cus = next_served_cus
    else:
        current_cus=unserved_cus[0]
        open_route=[]

    while len(unserved_cus) != 0:
        if not if_served(unserved_cus, current_cus):

            if int(open_route_load_kg) + int(instance.demand_kg[temp_unserved_cus.index(current_cus)+1]) > vehicles["payload"][
                vehicle_type[counter_vehicle]] or int(
                open_route_load_size) + int(instance.demand_size[temp_unserved_cus.index(current_cus)+1]) > vehicles["volume_area"][
                vehicle_type[counter_vehicle]] or float(open_route_distance) \
                    + float(distance_fromId_toId(instance, open_route[-2], current_cus)) \
                    + float(distance_fromId_toId(instance, current_cus, 0)) \
                    - float(distance_fromId_toId(instance, open_route[-2], 0)) > \
                    vehicles["reach"][vehicle_type[counter_vehicle]] or float(open_route_duration) \
                    + calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, open_route[-2], current_cus)) \
                    + calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, current_cus, 0)) \
                    - calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, open_route[-2], 0))\
                    + calculate_total_minutes_in_duration(instance.duration_S[temp_unserved_cus.index(current_cus)+1]) > shift_duration.get(city):

                solution.append(open_route)  # close the route once exceed the constraints and added into solution
                temp = random.randrange(0, 7)
                vehicle_type.append(temp)  # before opening a new route, generate a new vehicle type
                counter_vehicle += 1
                open_route = [0, current_cus, 0]  # open new route
                if if_route_feasible_before_assignment(open_route, instance, vehicle_type[counter_vehicle],temp_unserved_cus):
                    unserved_cus.remove(current_cus)  # customer is served and remove it from unserved_cus list
                    open_route_load_kg = int(instance.demand_kg[temp_unserved_cus.index(current_cus)+1])
                    open_route_load_size = int(instance.demand_size[temp_unserved_cus.index(current_cus)+1])
                    open_route_distance = float(distance_fromId_toId(instance, 0, current_cus)) \
                                          + float(distance_fromId_toId(instance, current_cus, 0))
                    open_route_duration = calculate_total_minutes_in_duration(
                        transportation_duration_fromId_toId(instance, 0, current_cus)) \
                                          + calculate_total_minutes_in_duration(
                        transportation_duration_fromId_toId(instance, current_cus, 0)) \
                                          + calculate_total_minutes_in_duration(instance.duration_S[temp_unserved_cus.index(current_cus)+1])
                else:  # this handles the case that the vehicle cannot serve even a single customer, and we change to
                    # the next vehicle type
                    open_route.remove(current_cus)
                    continue
            else:
                open_route.insert(-1, current_cus)
                open_route_load_kg = int(open_route_load_kg) + int(instance.demand_kg[temp_unserved_cus.index(current_cus)+1])
                open_route_load_size = int(open_route_load_size) + int(instance.demand_size[temp_unserved_cus.index(current_cus)+1])
                open_route_distance = float(open_route_distance) \
                                      + float(distance_fromId_toId(instance, open_route[-3], current_cus)) \
                                      + float(distance_fromId_toId(instance, current_cus, 0)) \
                                      - float(distance_fromId_toId(instance, open_route[-3], 0))
                open_route_duration = float(open_route_duration) + calculate_total_minutes_in_duration(
                    transportation_duration_fromId_toId(instance, open_route[-3], current_cus)) \
                                      + calculate_total_minutes_in_duration(
                    transportation_duration_fromId_toId(instance, current_cus, 0)) \
                                      - calculate_total_minutes_in_duration(
                    transportation_duration_fromId_toId(instance, open_route[-3], 0)) \
                                      + calculate_total_minutes_in_duration(instance.duration_S[temp_unserved_cus.index(current_cus)+1])
                unserved_cus.remove(current_cus)  # customer is served and remove it in unserved_cus list

        next_served_cus = find_neighbour(current_cus, unserved_cus, instance)
        current_cus = next_served_cus  # the nearst neighbour will be considered to be served

    solution.append(open_route)
    i = 0  # Counter for iterating vehicle type
    for route in solution:
        route.insert(0, vehicle_type[i] + 1)
        i += 1

    solution = list(filter(lambda r: len(r) > 3, solution))
    return solution


def check_feasibility_route(route: Route, city: str, instance: Instance) -> bool:
    vehicle_payload = vehicles["payload"]
    vehicle_volume = vehicles["volume_area"]
    vehicle_reach = vehicles["reach"]
    if calculate_route_demand_kg(route, instance) <= vehicle_payload[route[0] - 1] \
            and calculate_route_demand_size(route, instance) <= vehicle_volume[route[0] - 1] \
            and calculate_route_distance(route, instance) <= vehicle_reach[route[0] - 1] \
            and calculate_transportation_and_service_time(route, instance) <= shift_duration.get(city):
        feasibility = True
    else:
        feasibility = False
    return feasibility


def check_feasibility_sol(new_sol: List[List[int]], city: str, instance: Instance) -> bool:
    feasibility = list()
    for i in range(len(new_sol)):
        if check_feasibility_route(new_sol[i], city, instance):
            feasibility.append(True)
        else:
            feasibility.append(False)
    return all(feasibility)


def quantify_infeasibility(new_sol: List[List[int]], weighting_factor: int, city: str, instance: Instance) -> float:
    excess_total_weight = 0.0
    excess_total_volume = 0
    excess_total_distance = 0.0
    excess_total_duration = 0.0
    vehicle_payload = vehicles["payload"]
    vehicle_volume = vehicles["volume_area"]
    vehicle_reach = vehicles["reach"]

    for i in range(len(new_sol)):  # determining costs of capacity violation for every route of solution
        excess_route_weight = calculate_route_demand_kg(new_sol[i], instance) - vehicle_payload[new_sol[i][0] - 1]
        if excess_route_weight > 0.00001:
            excess_total_weight = excess_total_weight + excess_route_weight
        excess_route_volume = calculate_route_demand_size(new_sol[i], instance) - vehicle_volume[new_sol[i][0] - 1]
        if excess_route_volume > 0.00001:
            excess_total_volume = excess_total_volume + excess_route_volume
        excess_route_distance = calculate_route_distance(new_sol[i], instance) - vehicle_reach[new_sol[i][0] - 1]
        if excess_route_distance > 0.00001:
            excess_total_distance = excess_total_distance + excess_route_distance
        excess_route_duration = calculate_transportation_and_service_time(new_sol[i], instance) - shift_duration.get(
            city)
        if excess_route_duration > 0.00001:
            excess_total_duration = excess_total_duration + excess_route_duration

    excess_cost = weighting_factor * (excess_total_weight * 0.25 + excess_total_volume * 0.06 +
                                      excess_total_distance * 1.25 + excess_total_duration * 0.33)
    return excess_cost


def make_feasible(route: Route, city: str, instance: Instance) -> List[List[int]]:
    vehicle_payload = vehicles["payload"][route[0] - 1]
    vehicle_volume = vehicles["volume_area"][route[0] - 1]
    vehicle_reach = vehicles["reach"][route[0] - 1]
    customers = route[2:-1]
    sub_sol = list()

    new_route = [route[0], 0, customers[0], 0]
    sub_sol.append(new_route)
    new_route_weight = int(instance.demand_kg[create_unserved_cus(instance).index(customers[0])+1])
    new_route_volume = int(instance.demand_size[create_unserved_cus(instance).index(customers[0])+1])
    new_route_distance = float(distance_fromId_toId(instance, 0, customers[0])) \
                         + float(distance_fromId_toId(instance, customers[0], 0))
    new_route_duration = calculate_total_minutes_in_duration(
        transportation_duration_fromId_toId(instance, 0, customers[0])) \
                         + calculate_total_minutes_in_duration(instance.duration_S[create_unserved_cus(instance).index(customers[0])+1]) \
                         + calculate_total_minutes_in_duration(
        transportation_duration_fromId_toId(instance, customers[0], 0))

    for i in customers[1:]:
        if new_route_weight + int(instance.demand_kg[create_unserved_cus(instance).index(i)+1]) > vehicle_payload or new_route_volume + \
                int(instance.demand_size[create_unserved_cus(instance).index(i)+1]) > vehicle_volume or new_route_distance \
                + float(distance_fromId_toId(instance, new_route[-2], i)) \
                + float(distance_fromId_toId(instance, i, 0)) \
                - float(distance_fromId_toId(instance, new_route[-2], 0)) > vehicle_reach or new_route_duration + \
                + calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, new_route[-2], i)) \
                + calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, i, 0)) \
                - calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance, new_route[-2], 0)) \
                + calculate_total_minutes_in_duration(instance.duration_S[create_unserved_cus(instance).index(i)+1]) > shift_duration.get(city):
            new_route = [route[0], 0, i, 0]
            sub_sol.append(new_route)
            new_route_weight = int(instance.demand_kg[create_unserved_cus(instance).index(i)+1])
            new_route_volume = int(instance.demand_size[create_unserved_cus(instance).index(i)+1])
            new_route_distance = float(distance_fromId_toId(instance, 0, i)) \
                                 + float(distance_fromId_toId(instance, i, 0))
            new_route_duration = calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, 0, i)) \
                                 + calculate_total_minutes_in_duration(instance.duration_S[create_unserved_cus(instance).index(i)+1]) \
                                 + calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, i, 0))

        else:
            new_route.insert(-1, i)
            new_route_weight = new_route_weight + int(instance.demand_kg[create_unserved_cus(instance).index(i)+1])
            new_route_volume = new_route_volume + int(instance.demand_size[create_unserved_cus(instance).index(i)+1])
            new_route_distance = new_route_distance + float(distance_fromId_toId(instance, new_route[-3], i)) \
                                 + float(distance_fromId_toId(instance, i, 0)) \
                                 - float(distance_fromId_toId(instance, new_route[-3], 0))
            new_route_duration = new_route_duration \
                                 + calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, new_route[-3], i)) \
                                 + calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, i, 0)) \
                                 - calculate_total_minutes_in_duration(
                transportation_duration_fromId_toId(instance, new_route[-3], 0)) \
                                 + calculate_total_minutes_in_duration(instance.duration_S[create_unserved_cus(instance).index(i)+1])

    return sub_sol



def best_insertion(route: Route, customer: int, instance: Instance) -> int:
    shortest_distance = 1000000.0
    best_position = int
    for i in range(2, len(route)):
        distance = float(distance_fromId_toId(instance, route[i - 1], customer)) \
                   + float(distance_fromId_toId(instance, customer, route[i])) \
                   - float(distance_fromId_toId(instance, route[i - 1], route[i]))
        if distance < shortest_distance:
            shortest_distance = distance
            best_position = i
    assert shortest_distance < 1000000.0
    return best_position


def two_opt(solution: Solution, instance: Instance) -> Solution:
    for r_index, route in enumerate(solution):
        for i in range(2, len(route) - 1):
            for j in range(i + 1, len(route) - 1):
                change = float(distance_fromId_toId(instance, route[i - 1], route[j])) \
                         + float(distance_fromId_toId(instance, route[i], route[j + 1])) \
                         - float(distance_fromId_toId(instance, route[i - 1], route[i])) \
                         - float(distance_fromId_toId(instance, route[j], route[j + 1]))
                if change < -0.00001:
                    solution[r_index] = route[:i] + list(reversed(route[i:(j + 1)])) + route[(j + 1):]
    return solution


def get_new_sol(last_sol: List[List[int]], city: str, instance) -> List[List[int]]:  # milder version of get_new_sol
    last_sol = deepcopy(last_sol)
    chosen_option = random.choice(range(10))

    if chosen_option == 0:  # randomly replacing vehicle type of route
        chosen_vehicle = random.choice(range(1, 8))  # randomly choosing new vehicle type
        selected_route = random.choice(range(len(last_sol)))  # randomly choosing route to insert vehicle to
        last_sol[selected_route][0] = chosen_vehicle  # replacing current vehicle in chosen route with new vehicle
        if not check_feasibility_route(last_sol[selected_route], city, instance):  # if new route is not feasible
            feas_sol = make_feasible(last_sol[selected_route], city, instance)  # making feasible version of route
            if check_feasibility_sol(feas_sol, city, instance):  # checking if it is actually feasible
                last_sol.pop(selected_route)
                for i in range(len(feas_sol)):
                    last_sol.append(feas_sol[i])

    elif chosen_option in range(1, 4):  # randomly swapping customers between routes
        # randomly selecting two routes
        selected_routes = random.sample(range(len(last_sol)), 2)
        # randomly selecting one customer from each selected route via index
        i1 = random.choice(range(2, len(last_sol[selected_routes[0]]) - 1))
        i2 = random.choice(range(2, len(last_sol[selected_routes[1]]) - 1))
        # storing customers in variable
        customer1 = last_sol[selected_routes[0]][i1]
        customer2 = last_sol[selected_routes[1]][i2]
        # removing customers from old lists
        last_sol[selected_routes[0]].pop(i1)
        last_sol[selected_routes[1]].pop(i2)
        # inserting customers into new lists
        last_sol[selected_routes[0]].insert(best_insertion(last_sol[selected_routes[0]], customer2, instance),
                                            customer2)
        last_sol[selected_routes[1]].insert(best_insertion(last_sol[selected_routes[1]], customer1, instance),
                                            customer1)

    elif chosen_option in range(4, 7):  # randomly reversion one edge in a route
        selected_route = random.choice(range(len(last_sol)))  # randomly choosing route to reverse edge
        if len(last_sol[selected_route]) > 4:
            chosen_customer = random.choice(range(2, len(last_sol[selected_route]) - 1))
            if chosen_customer <= len(last_sol[selected_route]) - 3:
                i1 = chosen_customer
            else:
                i1 = chosen_customer - 1
            i2 = i1 + 1
            last_sol[selected_route] = last_sol[selected_route][:i1] + list(reversed(last_sol[selected_route][i1:(i2 + 1)])) \
            + last_sol[selected_route][(i2 + 1):]

    else:  # randomly inserting customer from one route into another
        selected_routes = random.sample(range(len(last_sol)), 2)  # randomly selecting two routes to swap customers from
        if len(last_sol[selected_routes[0]]) > 3:
            i1 = random.choice(
                range(2, len(last_sol[selected_routes[0]]) - 1))  # randomly selecting customer from first route
            customer1 = last_sol[selected_routes[0]][i1]  # storing customer in variable
            last_sol[selected_routes[0]].pop(i1)  # removing selected customer from first route
            last_sol[selected_routes[1]].insert(best_insertion(last_sol[selected_routes[1]], customer1, instance),
                                                customer1)  # inserting customer at best position in second route
            last_sol = deepcopy(last_sol)
            if len(last_sol[selected_routes[0]]) <= 3:  # removing empty list
                last_sol.pop(selected_routes[0])

    new_sol = last_sol  # storing new solution
    return new_sol

def simulated_annealing(initial_sol: List[List[int]], initial_temp: int, max_temp: int, max_rep: int,
                        temp_schedule: float, infeasibility_weight: int, instance: Instance, city: str,
                        city_toll: float) -> Solution:
    """
    :param initial_sol: solution created by nearest insertion heuristic
    :param initial_temp: initial annealing temperature
    :param max_temp: maximum number of temperature changes
    :param max_rep: maximum number of iterations per temperature
    :param temp_schedule: cooling factor
    :param infeasibility_weight: weighting factor for cost penalty of infeasibility
    :param instance: instance of city
    :param city: city the data originates from
    :param city_toll: toll for environmental zone in respective city for respective scenario
    :return: the best solution achieved
    """

    cost_last = total_cost(initial_sol, instance, city, city_toll)
    cost_best = total_cost(initial_sol, instance, city, city_toll)
    last_sol = initial_sol
    best_feas_sol = initial_sol
    t_k = initial_temp  # t_k: current temperature
    k = 0  # k: temperature change counter

    while k < max_temp and t_k >= 0.1:  # Park & Kim, 1998
        m = 0  # m: repetition change counter
        while m < max_rep:
            new_sol = get_new_sol(last_sol, city, instance)
            cost_new = total_cost(new_sol, instance, city, city_toll) \
                       + quantify_infeasibility(new_sol, infeasibility_weight, city, instance)
            # print(cost_new)
            delta = cost_new - cost_last
            if delta < -0.00001:
                last_sol = new_sol
                cost_last = cost_new
                # print(last_sol)
                # print(cost_last)
                # print(check_feasibility_sol(last_sol, city, instance))
                if cost_last <= cost_best:
                    best_sol = last_sol
                    cost_best = cost_new
                    if check_feasibility_sol(best_sol, city, instance):
                        best_feas_sol = best_sol
            else:
                y = random.uniform(0, 1)
                z = math.exp(-delta / t_k)
                if y < z:
                    last_sol = new_sol
                    cost_last = cost_new
                    # print(last_sol)
                    # print(cost_last)
                    # print(check_feasibility_sol(last_sol, city, instance))
            m += 1
        k += 1
        t_k = t_k - temp_schedule * t_k  # changing temperature
    return best_feas_sol
