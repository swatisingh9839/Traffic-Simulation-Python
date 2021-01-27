# Traffic system components


class Vehicle:
    """Represents vehicles in traffic simulations"""

    def __init__(self, destination, borntime):
        self.destination = destination
        self.borntime = borntime
        pass
    
    def __str__(self):
        pass

class Lane:
    "Represents a lane with (possible) vehicles"

    def __init__(self, length):
        self.time = 0
        self.emptyChar = '.'
        self.laneQueue = [self.emptyChar]*length
        self.maxIndex = length
        pass

    def __str__(self):

        #txtList =[]
        # for i in range(len(self.laneQueue)):
        #     if type(self.laneQueue[i]) == type(Vehicle('',0)):
        #         txtList.append(''.join(self.laneQueue[i].destination))
        #     else:
        #         txtList.append(''.join(self.laneQueue[i]))

        txtList = [(''.join(x.destination) if type(x) == type(Vehicle('',0)) else ''.join(x)) for x in self.laneQueue]
        return f"[{''.join(txtList)}]"


    def enter(self, vehicle):
        self.laneQueue[-1] = vehicle
        pass

    def last_free(self):
        if self.laneQueue[self.maxIndex-1] == ".":
            return True
        else:
            return False
        pass

    def step(self):
        self.time += 1
        for i in range(1, self.maxIndex):
            if self.laneQueue[i-1] == ".":
                self.laneQueue.insert(i-1, self.laneQueue.pop(i))
        pass

    def get_first(self):
        if self.laneQueue[0] != ".":
            return self.laneQueue[0]
        else:
            return None
        pass

    def remove_first(self):
        if self.laneQueue[0] != ".":
            data = self.laneQueue[0]
            self.laneQueue[0] = "."
            return data
            #return f"Vehicle{data.destination, data.borntime}"
        else:
            return None
        pass

    def number_in_lane(self):
        return len(self.laneQueue) - self.laneQueue.count(self.emptyChar)


def demo_lane():
    """For demonstration of the class Lane"""
    a_lane = Lane(10)
    print(a_lane)
    v = Vehicle('N', 34)
    a_lane.enter(v)
    print(a_lane)

    a_lane.step()
    print(a_lane)
    for i in range(20):
        if i % 2 == 0:
            u = Vehicle('S', i)
            a_lane.enter(u)
        a_lane.step()
        print(a_lane)
        if i % 3 == 0:
            print('  out: ',
                  a_lane.remove_first())
    print('Number in lane:',
          a_lane.number_in_lane())


class Light:
    """Represents a traffic light"""

    def __init__(self, period, green_period):
        self.period = period
        self.green_period = green_period
        self.time = 0
        self.periodCounter = 0
        pass

    def __str__(self):
        return "(G)"  if self.is_green() else "(R)"
        #return "a Light"

    def __repr__(self):
        pass

    def step(self):
        self.time += 1
        
        if(self.periodCounter < self.period-1):
            self.periodCounter += 1
        else:
            self.periodCounter = 0

        pass

    def is_green(self):
        if(self.periodCounter < self.green_period):
            return True
        else:
            return False  
        pass


def demo_light():
    """Demonstrats the Light class"""
    a_light = Light(7, 3)
    for i in range(15):
        print(i, a_light,
              a_light.is_green())
        a_light.step()


def main():
    """Demonstrates the classes"""
    print('\nLight demonstration\n')
    demo_light()
    print('\nLane demonstration')
    demo_lane()


if __name__ == '__main__':
    main()
