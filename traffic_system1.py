
from statistics import mean, median
from time import sleep
import destinations
import trafficComponents as tc


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):
        self.time = 0
        self.lane = tc.Lane(11)
        self.lane_west = tc.Lane(8)
        self.lane_south = tc.Lane(8)
        self.light_west = tc.Light(14, 6)
        self.light_south = tc.Light(14, 4)
        self.destination = destinations.Destinations()
        self.waitingQueue = []
        self.vehicleCreated = 0
        self.blockedCount = 0
        self.isBlocked = False
        self.queueCount = 0
        self.westVehicleDetails = {
            "vehicleOut": 0,
            "vehicleTime": []
        }
        self.southVehicleDetails = {
            "vehicleOut": 0,
            "vehicleTime": []
        }

    def __str__(self):
        txtList = [(x.destination) for x in self.waitingQueue]
        return f"{txtList}"

    def snapshot(self):
        print( f'{self.light_west} {self.lane_west}{"*" if self.isBlocked else " "}{self.lane}  {self}')
        print( f'{self.light_south} {self.lane_south}\n')

    def step(self):
        self.time += 1

        if self.light_west.is_green() and self.lane_west.get_first() is not None: # remove the first vehicle from west lane if west signal is green
            self.westVehicleDetails["vehicleOut"] += 1
            self.westVehicleDetails["vehicleTime"].append(self.time - self.lane_west.remove_first().borntime) # store the born time of the vehicle

        if self.light_south.is_green() and self.lane_south.get_first() is not None: # remove the first vehicle from south lane if south signal is green
            self.southVehicleDetails["vehicleOut"] += 1
            self.southVehicleDetails["vehicleTime"].append(self.time - self.lane_south.remove_first().borntime) # store the born time of the vehicle

        self.lane_west.step() # step the west lane
        self.lane_south.step() # step the south lane

        if self.lane.get_first() is not None: # check if the first slot is not empty
            if self.lane.get_first().destination == 'S' and self.lane_south.last_free(): # check if lane vehicle destination is South and last slot in lane south is empty
                self.lane_south.enter(self.lane.remove_first())
                self.isBlocked = False
            elif self.lane.get_first().destination == 'W' and self.lane_west.last_free(): # check if lane vehicle destination is West and last slot in lane west is empty
                self.lane_west.enter(self.lane.remove_first())
                self.isBlocked = False
            else: # it is blocked
                self.blockedCount += 1
                self.isBlocked = True

        self.lane.step() # step the lane

        des = self.destination.step()   

        if self.lane.last_free() and des != None and len(self.waitingQueue) == 0 : # check if the lane last slot is empty, des is not None and queue is empty
            newVeh = tc.Vehicle(des, self.time)
            self.vehicleCreated += 1
            self.lane.enter(newVeh)
        elif self.lane.last_free() and des != None and len(self.waitingQueue) != 0 : # check if the lane last slot is empty, des is not None and queue is not empty
            newVeh = tc.Vehicle(des, self.time)
            self.vehicleCreated += 1
            self.lane.enter(self.waitingQueue.pop(0))
            self.waitingQueue.append(newVeh)
            self.queueCount += 1
        elif not self.lane.last_free() and des != None: # check if the lane last slot is not empty, des is not None
            newVeh = tc.Vehicle(des, self.time)
            self.vehicleCreated += 1
            self.waitingQueue.append(newVeh)
            self.queueCount += 1
        elif self.lane.last_free() and des == None and len(self.waitingQueue) != 0: # check if the lane last slot is empty, des is None and queue is not empty
            self.lane.enter(self.waitingQueue.pop(0))


        self.light_south.step() #step the lights
        self.light_west.step() #step the lights

    def in_system(self):
        return self.lane.number_in_lane() + self.lane_south.number_in_lane() + self.lane_west.number_in_lane()

    def print_statistics(self):
        print("Statistics after 100 timesteps:")
        print()
        print(f"Created vehicles:    {self.vehicleCreated}")
        print(f"In system       :    {self.in_system()}")
        print()
        print("At exit         West        South")
        print(f"Vehicles out:    {self.westVehicleDetails['vehicleOut']}          {self.southVehicleDetails['vehicleOut']}")
        print(f"Minimal time:    {min(self.westVehicleDetails['vehicleTime'])}          {min(self.southVehicleDetails['vehicleTime'])}")
        print(f"Maximal time:    {max(self.westVehicleDetails['vehicleTime'])}          {max(self.southVehicleDetails['vehicleTime'])}")
        print(f"Mean time   :    {round(mean(self.westVehicleDetails['vehicleTime']),1)}        {round(mean(self.southVehicleDetails['vehicleTime']),1)}")
        print(f"Median time :    {round(median(self.westVehicleDetails['vehicleTime']),1)}          {round(median(self.southVehicleDetails['vehicleTime']),1)}")
        print()
        print(f"Blocked     : {round((self.blockedCount), 1)}%")
        print(f"Queue       : {round((self.queueCount/self.vehicleCreated)*100, 1)}%")
        pass


def main():
    ts = TrafficSystem()
    for i in range(100):
        ts.snapshot()
        ts.step()
        sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    main()
