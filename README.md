# Advanced Seminar - Sustainable Transportation Systems


## Simulated annealing & HVRP
A Python Implementation of a Simulated annealing-based Solution combining with nearest insertion heuristic algorithm to heterogenous Vehicle Routing Problem (HVRP) 

## Description
    1. Heterogenous Vehicle Routing Problem (HVRP) is a method for determining the optimal route of vehicles in order to serve customers starting from depot with various vehicle type.
    2. We need to determine routing solutions in three different cities: Paris, Shanghai and NewYork. There are several factors that affect the behaviour of routing:
            - the weight, volume of parcels and their needed service time as well as transportation time
            - the number of customers within one area
            - the geographical data like Longitude, latitude, and distance inside or outside of the city
    3. Customers in New York are separated into two data sets because of their geographical characteristics. Each city has over 100 customers.
    4. There are seven different vehicle types available while forming the routing clusters, including conventionally-powered Internal Combustion Engine Vehicles (ICEVs), Battery Electric Vehicles (BEVs) and Light Electric Freight Vehicles (LEFVs). Charactersitics like:
            - Payload
            - Loading area volume
            - Maximum reach 
            - Aquisition cost 
	        - etc. can influence the route design.
    5. Our main objective function is total cost of routes as a main evaluation criteria, which will be used in simulated annealing algorithm

## Installation
Python 3.9 / Python 3.10
Pip

## Instance Definition
Below is a description of the format of the data file that defines each problem instance. We just show city: Paris here:

```python
Id Lon Lat Demand[kg] Demand[m^3*10^-3] Duration
D0 2.4092229 48.9252582 0 0 00:00:00
C1 2.3322851 48.8279154 419 4191 00:15:00
C2 2.3987013 48.7936343 563 5631 00:16:00
...
C111 2.1798375 48.8794459 597 5971 00:19:00
C112 2.3170151 48.8146006 412 4121 00:12:00

```
```python
From To DistanceTotal[km] DistanceInside[km] DistanceOutside[km] Duration[s]
D0 D0 0 0 0 00:00:00
D0 C1 15.48 9.772 5.708 00:19:01
D0 C2 21.03 0.089 20.941 00:20:06
D0 C3 18.56 1.596 16.964 00:18:04
...
C112 C110 8.024 6.817 1.207 00:10:34
C112 C111 16.049 0 16.049 00:17:05
```
### Extract data 
For organizing the data and create instances for each city. We use function ```readNodes ``` and ```readRoute ``` under the file ```Reader.py ``` to extract the data from directory ```Data ```.
        
## Visualization
We used function ```draw_routes ``` file ```Plot.py ``` to visualize the generated result.


## Nearest Insertion Heuristics
The general processes of the nearest insertion heuristic here are randomly choosing one vehicle and forming the route clusters by selecting customers. We want to have the output of this heuristic method as initial route candidates for simulated annealing algorithm.

Following is code example of this method:
```
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
    temp_unserved_cus=List.copy(unserved_cus)

    current_cus = unserved_cus[0]
    vehicle_type = [random.randrange(0, 7)]  # a list to save generated vehicle types
    counter_vehicle = 0  # counter of vehicle_type list
    open_route = [0, unserved_cus[0], 0]
    solution = list()
```

Functions under file ```Construction.py``` like ```distance_fromId_toId```, ```if_route_feasible_before_assignment```, ```find_neighbour```, ```if_served```, ```create_unserved_cus``` are helping functions for  ```nearest_neighbourhood```. 

The specific goals of each functions can be found within comments of the file ```Construction.py```


## Simulated Annealing Implmentation
We generate our final solutions for each instance using function ```simulated_annealing``` under the file ```Construction.py```. Following is the brief descriptions of the parameters we used:

    param initial_sol: solution created by savings heuristic
    param initial_temp: initial annealing temperature
    param max_temp: maximum number of temperature changes
    param max_rep: maximum number of iterations per temperature
    param temp_schedule: cooling factor
    param infeasibility_weight: weighting factor for cost penalty of infeasibility
    param instance: instance of city
    param city: city the data originates from
    param city_toll: toll for environmental zone in respective city for respective scenario
    return: the best solution achieved

We need both functions for creating new possible candidate solutions and the functions to evaluate the feasiblity of candidates. Functions like ```best_insertion```, ```two_opt```,```get_new_sol``` aim at providing large solutions pool for simulated annealing. Other functions like ```make_feasible```, ```quantify_infeasibility```, ```check_feasibility_sol```,```check_feasibility_route``` make sure that we have one final feasible solution as output as well as guiding the movement of simulated annealing.

Below is the code example of ```get_new_sol```, which is the main helping function for Simulated annealing:
```
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
...

```


## Evaluation

Function ```total_cost``` is the main evaluation criteria for finding the final feasible solution for each city. For calculating total cost, we calculate:
    - `operational_cost` - A cost which include driving costs(The transportation cost of one vehicle for a unit distance) and maintenance costs depends on vehicle type and routes
    - `daily_utility_costs` - A cost which includes acquisition and resell of the vehicles
    - `wage_costs` - A payment for drivers in different cities per day.
    - `tolling_costs` - A cost which happens because of the conventionally-powered Internal Combustion Engine Vehicles (one vehicle for a unit distance)

All related functiosn can be found under the file `Objectives.py`


## File Structure
```
├── data/
│   ├── NewYork.1.nodes
│   │── NewYork.2.nodes
│   ├── NewYork.routes
│   │── Paris.nodes
│   │── Paris.routes
│   ├── Shanghai.nodes
│   │── Shanghai.routes
├── Construction.py
├── main.py
├── Objectives.py
├── Plot.py
├── Reader.py
├── README.md
```


## Authors and acknowledgment
Group 4 members: Syrine Ben Abda, Daniel Jaumann, Minyi Huang​ have contributed the algorithm implementation.

## License
[MIT](https://choosealicense.com/licenses/mit/)

