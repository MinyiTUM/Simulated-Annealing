#   Capacitated Vehicle Routing Problem
#   Execution solutions and showing plots
#   Goal is to minimize the cost by shorten total distance traveled, having
#   suitable fleet combination OR minimize the service+travelling time

# import math
# import sys
# import os
import time
from typing import Any, List
from Construction import *
from Plot import *
from Reader import *
from Objectives import *


def main(args: list[str]):
    # getting the start wall time
    st_wall = time.time()
    # getting the start CPU time
    # get the start time
    st_cpu = time.process_time()

    nodes_Paris: Any = readNodes(args[1])
    routes_Paris: Any = readRoute(args[2])
    # nodes_Shanghai: Any = readNodes(args[1])
    # routes_Shanghai: Any = readRoute(args[2])
    # nodes_New_York1: Any = readNodes(args[1])
    # nodes_New_York2: Any = readNodes(args[1])
    # routes_NewYork: Any = readRoute(args[2])

    # 2 Extract data from the files and create instance (organize the data)
    # Paris

    id = nodes_Paris['id']
    demand_weight: list[int] = list()
    for item in nodes_Paris['demand_weight']:
        demand_weight.append(item)

    demand_size: list[int] = nodes_Paris['demand_size']
    duration_S = nodes_Paris['duration_S']
    from_id = routes_Paris['from_id']
    to_id = routes_Paris['to_id']
    distance_total = routes_Paris['distance_total']
    distance_inside = routes_Paris['distance_inside']
    distance_outside = routes_Paris['distance_outside']
    duration_T = routes_Paris['duration_T']

    instance = Instance(id, demand_weight, demand_size, duration_S, from_id, to_id, distance_total, distance_inside,
                        distance_outside, duration_T)

    initial_sol0 = nearest_neighbourhood(instance, "Paris")
    initial_sol = two_opt(initial_sol0, instance)
    print(initial_sol)
    print("Initial costs:", total_cost(initial_sol, instance, "Paris", 0.1))
    print(check_feasibility_sol(initial_sol, "Paris", instance))

    annealing_sol = simulated_annealing(initial_sol, 20, 500, 50, 0.01, 10, instance, "Paris", 0.4)
    print(annealing_sol)
    print("Final costs_paris:", total_cost(annealing_sol, instance, "Paris", 0.1))
    print(draw_routes(annealing_sol, nodes_Paris))

    print("Initial number of routes_paris:", len(initial_sol))
    print("Final number of routes_paris:", len(annealing_sol))

    k = 0
    for i in range(len(annealing_sol)):
        for j in annealing_sol[i][2:-1]:
            k += 1
    print("Final number of customers served_paris:", k)

    unique_list = []
    for i in range(len(annealing_sol)):
        for j in annealing_sol[i]:
            if j not in unique_list:
                unique_list.append(j)
    unique_list.remove(0)
    print("Final number of unique customers served", len(unique_list))

    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    v5 = 0
    v6 = 0
    v7 = 0
    for i in annealing_sol:
        if i[0] == 1:
            v1 += 1
        elif i[0] == 2:
            v2 += 1
        elif i[0] == 3:
            v3 += 1
        elif i[0] == 4:
            v4 += 1
        elif i[0] == 5:
            v5 += 1
        elif i[0] == 6:
            v6 += 1
        else:
            v7 += 1
    print("Vehicles type 1:", v1)
    print("Vehicles type 2:", v2)
    print("Vehicles type 3:", v3)
    print("Vehicles type 4:", v4)
    print("Vehicles type 5:", v5)
    print("Vehicles type 6:", v6)
    print("Vehicles type 7:", v7)

    # getting the end wall time
    et_wall = time.time()
    # getting the end CPU time
    et_cpu = time.process_time()
    # getting the wall execution time
    elapsed_time = et_wall - st_wall
    print('Wall execution time:', elapsed_time, 'seconds')
    # getting the CPU execution time
    res = et_cpu - st_cpu
    print('CPU execution time:', res, 'seconds')


    # # Shanghai
    # id_Shanghai = nodes_Shanghai['id']
    # demand_weight_Shanghai: list[int] = nodes_Shanghai['demand_weight']
    # demand_size_Shanghai: list[int] = nodes_Shanghai['demand_size']
    # duration_S_Shanghai = nodes_Shanghai['duration_S']
    # from_id_Shanghai = routes_Shanghai['from_id']
    # to_id_Shanghai = routes_Shanghai['to_id']
    # distance_total_Shanghai = routes_Shanghai['distance_total']
    # distance_inside_Shanghai = routes_Shanghai['distance_inside']
    # distance_outside_Shanghai = routes_Shanghai['distance_outside']
    # duration_T_Shanghai = routes_Shanghai['duration_T']
    # 
    # instance_Shanghai = Instance(id_Shanghai, demand_weight_Shanghai, demand_size_Shanghai, duration_S_Shanghai,
    #                              from_id_Shanghai, to_id_Shanghai, distance_total_Shanghai, distance_inside_Shanghai,
    #                              distance_outside_Shanghai, duration_T_Shanghai)
    # 
    # initial_sol_Shanghai = nearest_neighbourhood(instance_Shanghai, "Shanghai")
    # print(initial_sol_Shanghai)
    # print("Initial costs_Shanghai:", total_cost(initial_sol_Shanghai, instance_Shanghai, "Shanghai", 0.1))
    # 
    # annealing_sol_Shanghai = simulated_annealing(initial_sol_Shanghai, 50, 100, 10, 0.01, 10, instance_Shanghai,
    #                                              "Shanghai", 0.1)
    # 
    # print(annealing_sol_Shanghai)
    # print("Final costs_Shanghai:", total_cost(annealing_sol_Shanghai, instance_Shanghai, "Shanghai", 0.1))
    # print(draw_routes(annealing_sol_Shanghai, nodes_Shanghai))
    # 
    # print("Initial number of routes_Shanghai:", len(initial_sol_Shanghai))
    # print("Final number of routes_Shanghai:", len(annealing_sol_Shanghai))
    # 
    # k = 0
    # for i in range(len(annealing_sol_Shanghai)):
    #     for j in annealing_sol_Shanghai[i][2:-1]:
    #         k += 1
    # print("Final number of customers served_Shanghai:", k)
    # 
    # #print("duration test:",calculate_total_minutes_in_duration(transportation_duration_fromId_toId(instance,0, 4)))
    # #initial_sol = nearest_neighbourhood(instance,"Paris")
    # #print(initial_sol)
    # 
    # 
    # #New_York1
    # id_New_York1 = nodes_New_York1['id']
    # demand_weight_New_York1: list[int] = nodes_New_York1['demand_weight']
    # demand_size_New_York1: list[int] = nodes_New_York1['demand_size']
    # duration_S_New_York1 = nodes_New_York1['duration_S']
    # from_id_New_York1 = routes_NewYork['from_id']
    # to_id_New_York1 = routes_NewYork['to_id']
    # distance_total_New_York1 = routes_NewYork['distance_total']
    # distance_inside_New_York1 = routes_NewYork['distance_inside']
    # distance_outside_New_York1 = routes_NewYork['distance_outside']
    # duration_T_New_York1 = routes_NewYork['duration_T']
    # 
    # instance_New_York1 = Instance(id_New_York1, demand_weight_New_York1, demand_size_New_York1, duration_S_New_York1,
    #                              from_id_New_York1, to_id_New_York1, distance_total_New_York1, distance_inside_New_York1,
    #                              distance_outside_New_York1, duration_T_New_York1)
    # 
    # initial_sol_New_York1 = nearest_neighbourhood(instance_New_York1, "New_York")
    # print(initial_sol_New_York1)
    # print("Initial costs_Shanghai:", total_cost(initial_sol_New_York1, initial_sol_New_York1, "New_York", 0.1))
    # 
    # annealing_sol_New_York1 = simulated_annealing(initial_sol_New_York1, 50, 100, 10, 0.01, 10, initial_sol_New_York1,
    #                                              "New_York", 0.1)
    # 
    # print(annealing_sol_New_York1)
    # print("Final costs_Shanghai:", total_cost(annealing_sol_New_York1, instance_New_York1, "New_York", 0.1))
    # print(draw_routes(annealing_sol_New_York1, nodes_New_York1))
    # 
    # print("Initial number of routes_Shanghai:", len(initial_sol_New_York1))
    # print("Final number of routes_Shanghai:", len(annealing_sol_New_York1))
    # 
    # k = 0
    # for i in range(len(annealing_sol_New_York1)):
    #     for j in annealing_sol_New_York1[i][2:-1]:
    #         k += 1
    # print("Final number of customers served_New_York1:", k)
    # 
    # # New_York2
    # id_New_York2 = nodes_New_York2['id']
    # demand_weight_New_York2: list[int] = nodes_New_York2['demand_weight']
    # demand_size_New_York2: list[int] = nodes_New_York2['demand_size']
    # duration_S_New_York2 = nodes_New_York2['duration_S']
    # from_id_New_York2 = routes_NewYork['from_id']
    # to_id_New_York2 = routes_NewYork['to_id']
    # distance_total_New_York2 = routes_NewYork['distance_total']
    # distance_inside_New_York2 = routes_NewYork['distance_inside']
    # distance_outside_New_York2 = routes_NewYork['distance_outside']
    # duration_T_New_York2 = routes_NewYork['duration_T']
    # 
    # instance_New_York2 = Instance(id_New_York2, demand_weight_New_York2, demand_size_New_York2, duration_S_New_York2,
    #                               from_id_New_York2, to_id_New_York2, distance_total_New_York2,
    #                               distance_inside_New_York2,
    #                               distance_outside_New_York2, duration_T_New_York2)
    # 
    # initial_sol_New_York2 = nearest_neighbourhood(instance_New_York2, "New_York")
    # print(initial_sol_New_York2)
    # print("Initial costs_Shanghai:", total_cost(initial_sol_New_York2, initial_sol_New_York2, "New_York", 0.1))
    # 
    # annealing_sol_New_York2 = simulated_annealing(initial_sol_New_York2, 50, 100, 10, 0.01, 10, initial_sol_New_York2,
    #                                               "New_York", 0.1)
    # 
    # print(annealing_sol_New_York2)
    # print("Final costs_Shanghai:", total_cost(annealing_sol_New_York2, instance_New_York2, "New_York", 0.1))
    # print(draw_routes(annealing_sol_New_York2, nodes_New_York2))
    # 
    # print("Initial number of routes_Shanghai:", len(initial_sol_New_York2))
    # print("Final number of routes_Shanghai:", len(annealing_sol_New_York2))
    # 
    # k = 0
    # for i in range(len(annealing_sol_New_York2)):
    #     for j in annealing_sol_New_York2[i][2:-1]:
    #         k += 1
    # print("Final number of customers served_New_York1:", k)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
