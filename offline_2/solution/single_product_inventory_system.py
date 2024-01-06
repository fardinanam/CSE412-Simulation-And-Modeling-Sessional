import rand
class SingleProductInventorySystem:
    def __init__(self, initial_inventory_level : int, num_months : int, num_policies : int, num_values_demand : int, mean_interdemand : float, setup_cost : float, incremental_cost : float, holding_cost : float, shortage_cost : float, minlag : float, maxlag : float, prob_distrib_demand : list, small_policies : list, big_policies : list, output_filename : str = "out.txt"):
        # input validation
        assert len(prob_distrib_demand) == num_values_demand
        assert len(small_policies) == num_policies and len(big_policies) == num_policies
        assert minlag <= maxlag
        assert num_months > 0 and num_policies > 0 and num_values_demand > 0 and mean_interdemand > 0 and setup_cost > 0 and incremental_cost > 0 and holding_cost > 0 and shortage_cost > 0

        for i in range(num_values_demand):
            assert prob_distrib_demand[i] >= 0 and prob_distrib_demand[i] <= 1
        
        for i in range(num_policies):
            assert small_policies[i] <= big_policies[i]

        # class variables
        self.num_events = 4
        self.initial_inventory_level = initial_inventory_level
        self.num_months = num_months
        self.num_policies = num_policies
        self.num_values_demand = num_values_demand
        self.mean_interdemand = mean_interdemand
        self.setup_cost = setup_cost
        self.incremental_cost = incremental_cost
        self.holding_cost = holding_cost
        self.shortage_cost = shortage_cost
        self.minlag = minlag
        self.maxlag = maxlag  
        self.prob_distrib_demand = prob_distrib_demand
        self.small_policies = small_policies
        self.big_policies = big_policies

        self.output_filename = output_filename

    def __init_sim_vars__(self):
        # simulation clock
        self.sim_time = 0.0

        # state variables
        self.inventory_level = self.initial_inventory_level
        self.time_last_event = 0.0
        self.next_event_type = 0

        # statistical counters
        self.total_ordering_cost = 0.0
        self.area_holding = 0.0
        self.area_shortage = 0.0

        # event list
        self.time_next_event = [
            None,
            1.0e30,
            self.sim_time + rand.expon(self.mean_interdemand),
            self.num_months,
            0.0
        ]

    def __init_report__(self):
        with open(self.output_filename, 'w') as out:
            out.write("------Single-Product Inventory System------\n\n")
            out.write(f"Initial Inventory Level: {self.initial_inventory_level} items\n\n")
            out.write(f"Number of demand sizes: {self.num_values_demand}\n\n")

            out.write(f"Distribution function of demand sizes: ")
            for i in range(self.num_values_demand):
                out.write(f"{self.prob_distrib_demand[i]} ")

            out.write(f"\n\nMean inter-demand time: {self.mean_interdemand} months\n\n")
            out.write(f"Delivery Lag Range: {self.minlag} to {self.maxlag} months\n\n")
            out.write(f"Length of the simulation: {self.num_months} months\n\n")
            out.write(f"K ={self.setup_cost:6.1f}\ni ={self.incremental_cost:6.1f}\nh ={self.holding_cost:6.1f}\npi ={self.shortage_cost:6.1f}\n\n")
            out.write(f"Number of policies: {self.num_policies}\n\n")
            out.write("------------------------------------------------------------------------\n")
            out.write("                 Average        Average")
            out.write("        Average        Average\n")
            out.write("  Policy       total cost    ordering cost")
            out.write("  holding cost   shortage cost\n")
            out.write("------------------------------------------------------------------------\n")

    def __timing__(self):
        min_time_next_event = 1.0e+29
        self.next_event_type = 0

        for i in range(1, self.num_events + 1):
            if self.time_next_event[i] < min_time_next_event:
                min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        if self.next_event_type == 0:
            print(f"Event list empty at time {self.sim_time}")
            exit(1)

        self.sim_time = min_time_next_event

    def __update_time_avg_stats__(self):
        time_since_last_event = self.sim_time - self.time_last_event

        self.time_last_event = self.sim_time

        if self.inventory_level < 0:
            self.area_shortage -= self.inventory_level * time_since_last_event
        elif self.inventory_level > 0:
            self.area_holding += self.inventory_level * time_since_last_event

    def __order_arrival__(self):
        self.inventory_level += self.amount_ordered

        self.time_next_event[1] = 1.0e+30

    def __demand_occurs__(self):
        demand = rand.random_integer(self.prob_distrib_demand)
        self.inventory_level -= demand

        self.time_next_event[2] = self.sim_time + rand.expon(self.mean_interdemand)

    def __evaluate__(self):
        #  Check whether the inventory level is less than smalls.
        if self.inventory_level < self.smalls:
            self.amount_ordered = self.bigs - self.inventory_level
            self.total_ordering_cost += self.setup_cost + self.incremental_cost * self.amount_ordered

            self.time_next_event[1] = self.sim_time + rand.uniform(self.minlag, self.maxlag)
        
        self.time_next_event[4] = self.sim_time + 1.0

    def __report__(self):
        avg_ordering_cost = self.total_ordering_cost / self.num_months
        avg_holding_cost = self.holding_cost * self.area_holding / self.num_months
        avg_shortage_cost = self.shortage_cost * self.area_shortage / self.num_months
        avg_total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost

        with open(self.output_filename, 'a') as out:
            out.write(f"\n({self.smalls:3d},{self.bigs:3d}){avg_total_cost:15.2f}{avg_ordering_cost:15.2f}{avg_holding_cost:15.2f}{avg_shortage_cost:15.2f}\n")

    def run(self):
        self.__init_report__()

        for i in range(self.num_policies):
            self.smalls = self.small_policies[i]
            self.bigs = self.big_policies[i]
            self.__init_sim_vars__()

            while (True):
                # determine the next event
                self.__timing__()

                # update time-average statistical accumulators
                self.__update_time_avg_stats__()

                # invoke the appropriate event function
                if self.next_event_type == 1:
                    self.__order_arrival__()
                elif self.next_event_type == 2:
                    self.__demand_occurs__()
                elif self.next_event_type == 3:
                    self.__report__()
                    break
                elif self.next_event_type == 4:
                    self.__evaluate__()
