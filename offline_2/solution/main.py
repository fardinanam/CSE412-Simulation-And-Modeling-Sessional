from single_product_inventory_system import SingleProductInventorySystem
import sys

if __name__ == "__main__":
    initial_inventory_level = 0
    num_months = 0
    num_policies = 0
    num_values_demand = 0
    mean_interdemand = 0.0
    setup_cost = 0.0
    incremental_cost = 0.0
    holding_cost = 0.0
    shortage_cost = 0.0
    minlag = 0.0
    maxlag = 0.0
    prob_distrib_demand = []
    small_policies = []
    big_policies = []

    # take input filename from command line
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_filename>")
        exit(1)

    input_filename = sys.argv[1]

    try:
        with open(input_filename, "r") as f:
            line = f.readline()
            inputs = line.split(" ")
            initial_inventory_level = int(inputs[0])
            num_months = int(inputs[1])
            num_policies = int(inputs[2])

            line = f.readline()
            inputs = line.split(" ")
            num_values_demand = int(inputs[0])
            mean_interdemand = float(inputs[1])

            line = f.readline()
            inputs = line.split(" ")
            setup_cost = float(inputs[0])
            incremental_cost = float(inputs[1])
            holding_cost = float(inputs[2])
            shortage_cost = float(inputs[3])

            line = f.readline()
            inputs = line.split(" ")
            minlag = float(inputs[0])
            maxlag = float(inputs[1])

            line = f.readline()
            prob_distrib_demand = list(map(float, line.split(" ")))

            line = f.readlines()
            for i in range(num_policies):
                inputs = line[i].split(" ")
                small_policies.append(int(inputs[0]))
                big_policies.append(int(inputs[1]))
    except:
        print("Error reading input file")
        exit(1)

    spis = SingleProductInventorySystem(initial_inventory_level, num_months, num_policies, num_values_demand, mean_interdemand, setup_cost, incremental_cost, holding_cost, shortage_cost, minlag, maxlag, prob_distrib_demand, small_policies, big_policies)

    spis.run()