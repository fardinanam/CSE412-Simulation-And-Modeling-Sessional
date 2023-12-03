import math
from enum import Enum
import pmmlcg


class ServerStatus(Enum):
    IDLE = 0
    BUSY = 1

class SingleServerQueue:
    def __init__(self, mean_interarrival, mean_service, num_delays_required):
        # output files
        self.event_orders_filename = "event_orders.txt"
        self.stats_filename = "results.txt"

        self.Q_LIMIT = 100
        self.time_arrival = [0.0] * (self.Q_LIMIT + 1)
        self.next_event_type = 0

        # simulation parameters
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.num_delays_required = num_delays_required

        # simulation clock
        self.sim_time = 0.0

        # state variables
        self.server_status = ServerStatus.IDLE
        self.num_in_queue = 0
        self.time_last_event = 0.0
        self.total_events_occurred = 0
        self.total_customers_arrived = 0
        self.total_customers_departed = 0

        # statistical counters
        self.num_customers_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_queue = 0.0
        self.area_server_status = 0.0

        # event list
        self.time_next_event = [0.0] * 3
        self.__update_next_arrival_time__() # first arrival time
        self.time_next_event[2] = 1.0e+30 # first departure time (infinity)

        # initialize event output files
        open(self.event_orders_filename, "w").close()
        open(self.stats_filename, "w").close()

    def __random__(self, mean):
        return -mean * math.log(pmmlcg.lcgrand(1))
    
    def __update_next_arrival_time__(self):
        self.time_next_event[1] = self.sim_time + self.__random__(self.mean_interarrival)
    
    def __update_next_departure_time__(self):
        self.time_next_event[2] = self.sim_time + self.__random__(self.mean_service)

    def timing(self):
        min_time_next_event = 1.0e+29
        self.next_event_type = 0
        num_events = 2 # arrival, departure

        for i in range(1, num_events + 1):
            if self.time_next_event[i] < min_time_next_event:
                min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        if self.next_event_type == 0:
            print(f"Event list empty at time {self.sim_time}")
            exit(1)
        
        self.total_events_occurred += 1

        self.sim_time = min_time_next_event

    def arrive(self):
        self.__update_next_arrival_time__()
        self.total_customers_arrived += 1

        with open(self.event_orders_filename, "a") as f:
            f.write(f"{self.total_events_occurred}. Next event: Customer {self.total_customers_arrived} Arrival\n")

        if self.server_status == ServerStatus.BUSY:
            """
            Server is busy, so increment number of customers in queue.
            """
            self.num_in_queue += 1

            if self.num_in_queue > self.Q_LIMIT:
                """
                The queue has overflowed, so stop the simulation.
                """
                print("Overflow of the array time_arrival at")
                print(f"time {self.sim_time}")
                exit(2)

            self.time_arrival[self.num_in_queue] = self.sim_time
        else:
            """
            Server is idle, so arriving customer has a delay of zero. (No need to add delay to total_of_delays.)
            """
            # delay = 0.0
            # self.total_of_delays += delay

            self.num_customers_delayed += 1
            self.server_status = ServerStatus.BUSY

            self.__update_next_departure_time__()

            with open(self.event_orders_filename, "a") as f:
                f.write(f"\n---------No. of customers delayed: {self.num_customers_delayed}--------\n\n")

    def depart(self):
        self.total_customers_departed += 1

        with open(self.event_orders_filename, "a") as f:
            f.write(f"{self.total_events_occurred}. Next event: Customer {self.total_customers_departed} Departure\n")

        if self.num_in_queue == 0:
            """
            The queue is empty so make the server idle and eliminate the
            departure (service completion) event from consideration.
            """
            self.server_status = ServerStatus.IDLE
            self.time_next_event[2] = 1.0e+30
        else:
            """
            The queue is nonempty, so decrement the number of customers in
            queue.
            """
            self.num_in_queue -= 1

            delay = self.sim_time - self.time_arrival[1]
            self.total_of_delays += delay

            self.num_customers_delayed += 1

            self.__update_next_departure_time__()
            with open(self.event_orders_filename, "a") as f:
                f.write(f"\n---------No. of customers delayed: {self.num_customers_delayed}--------\n\n")
                

            for i in range(1, self.num_in_queue + 1):
                self.time_arrival[i] = self.time_arrival[i + 1]

    def report(self):        
        with open(self.stats_filename, "w") as f:
            f.write(f"Average delay in queue: {self.total_of_delays / self.num_customers_delayed}\n")
            f.write(f"Average number in queue: {self.area_num_in_queue / self.sim_time}\n")
            f.write(f"Server utilization: {self.area_server_status / self.sim_time}\n")
            f.write(f"Time simulation ended: {self.sim_time}\n")

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time

        self.area_num_in_queue += self.num_in_queue * time_since_last_event
        self.area_server_status += self.server_status.value * time_since_last_event

    def run(self):

        while self.num_customers_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()

            if self.next_event_type == 1:
                self.arrive()

            elif self.next_event_type == 2:
                self.depart()

        self.report()


if __name__ == "__main__":
    with open("in.txt", "r") as f:
        lines = f.readlines()
        inputs = list(map(float, lines[0].split(" ")))
        mean_interarrival = inputs[0]
        mean_service = inputs[1]
        num_delays_required = int(inputs[2])

    single_server_queue = SingleServerQueue(mean_interarrival, mean_service, num_delays_required)
    single_server_queue.run()