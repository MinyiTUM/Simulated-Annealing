###
# Read data files(node files & route files) from New York, Paris and Shanghai


def readNodes(path):
    '''

    :param path: path of targeted file
    :return: dic data type with id, x(lon), y(lat), demand(weight), demand(volume), duration(service time)
    '''
    id=list()
    x=list()
    y=list()
    demand_weight=list()
    demand_size=list()
    duration_S=list()
    with open(path, "r") as file:
        lines = file.read().splitlines()
        for k in range(1,len(lines)):
            id.append(lines[k].split()[0])
            x.append(float(lines[k].split()[1]))
            y.append(float(lines[k].split()[2]))
            demand_weight.append(lines[k].split()[3])
            demand_size.append(lines[k].split()[4])
            duration_S.append(lines[k].split()[5])
    return {'id':id,'x':x,'y':y,'demand_weight':demand_weight,'demand_size':demand_size,'duration_S':duration_S}

def readRoute(path):
    '''

        :param path: path of targeted file
        :return: dic data type with from_id, to_id, distanceTotal, distanceInside, ddistanceOutside, duration(travelling time)
    '''
    from_id=list()
    to_id=list()
    distance_total = list()
    distance_inside = list()
    distance_outside = list()
    duration_T=list()
    with open(path, "r") as file:
        lines = file.read().splitlines()
        for k in range(1,len(lines)):
            from_id.append(lines[k].split()[0])
            to_id.append(lines[k].split()[1])
            distance_total.append(lines[k].split()[2])
            distance_inside.append(lines[k].split()[3])
            distance_outside.append(lines[k].split()[4])
            duration_T.append(lines[k].split()[5])
    return {'from_id':from_id,'to_id':to_id,'distance_total':distance_total,'distance_inside':distance_inside,'distance_outside':distance_outside,'duration_T':duration_T}
