
from statistics import mean, median
from time import sleep
import destinations
import trafficComponents as tc


class TrafficSystem:
    """Defines a traffic system"""

    def __init__(self):
        self.time = 0
        self.lane1 = tc.Lane(5)
        self.lane2 = tc.Lane(5)
        self.trafficLight = tc.Light(10,8)
        self.destination = destinations.Destinations()
        self.waitingQueue = []

    def __str__(self):
        txtList = [(x.destination) for x in self.waitingQueue]
        return f"{txtList}"

    def snapshot(self):
        print( f' {self.lane1}{self.trafficLight} {self.lane2}   {self}')

    def step(self):
        self.time += 1
        self.lane1.remove_first()
        self.lane1.step()
        if(self.trafficLight.is_green()):
            if(self.lane2.get_first() != None):
                self.lane1.enter(self.lane2.remove_first())
        
        self.trafficLight.step()
        self.lane2.step()
        
        des = self.destination.step()      

        if self.lane2.last_free() and des != None and len(self.waitingQueue) == 0 : # check if the lane2 last slot is empty, des is not None and queue is empty
            newVeh = tc.Vehicle(des, self.time)
            self.lane2.enter(newVeh)
        elif self.lane2.last_free() and des != None and len(self.waitingQueue) != 0 : # check if the lane2 last slot is empty, des is not None and queue is not empty
            newVeh = tc.Vehicle(des, self.time)
            self.lane2.enter(self.waitingQueue.pop(0))
            self.waitingQueue.append(newVeh)
        elif not self.lane2.last_free() and des != None: # check if the lane2 last slot is not empty, des is not None
            newVeh = tc.Vehicle(des, self.time)
            self.waitingQueue.append(newVeh)
        elif self.lane2.last_free() and des == None and len(self.waitingQueue) != 0: # check if the lane2 last slot is empty, des is None and queue is not empty
            self.lane2.enter(self.waitingQueue.pop(0))
        else:
            pass

    def in_system(self):
        pass

    def print_statistics(self):
        pass


def main():
    ts = TrafficSystem()
    for i in range(34):
        ts.snapshot()
        ts.step()
        sleep(0.1)
    print('\nFinal state:')
    ts.snapshot()
    print()
    ts.print_statistics()


if __name__ == '__main__':
    main()
