import csv
import random

class Item:

    def __init__(self, name, points, weight, volume):
        self.name = name
        self.weight = weight
        self.volume = volume
        self.points = points
    
    def __repr__(self):
        return self.name

    def get_weight(self):
        return self.weight
    
    def get_volume(self):
        return self.volume
    
    def get_points(self):
        return self.points


class Items:

    def __init__(self):
        self.item_list = []
        self.current = len(self.item_list) - 1
    
    def add_item(self, *args):
        for item in args:
            self.item_list.append(item)
    
    def get_total_points(self):
        sum = 0

        for item in self.item_list:
            sum += item.get_points()

        return sum
    
    def get_item_on_index(self, index) -> Item:
        return self.item_list[index] if self.index_is_within_bounds(index) else None
    
    def remove_item(self, item: Item):
         if item in self.item_list:
            self.item_list.remove(item)

    def get_items(self):
        return self.item_list
    
    def index_is_within_bounds(self, index):
        return index > len(self.item_list) or  index < (-1 * len(self.item_list))
    
    def is_empty(self):
        return len(self.item_list) == 0

class Resources:

    def __init__(self, weight_available, volume_available):
        self.remaining_weight = weight_available
        self.remaining_volume = volume_available
    
    def update_resources(self, item: Item):
        if self.has_enough_resources(item):
            self.remaining_weight -= item.get_weight()
            self.remaining_volume -= item.get_volume()
            return True
        else:
            return False
    
    def has_enough_resources(self, item: Item):
        return item.get_weight() <= self.remaining_weight and item.get_volume() <= self.remaining_volume

    def get_remaining_weight(self):
        return self.remaining_weight
    
    def get_remaining_volume(self):
        return  self.remaining_volume


class Knapsack:

    def __init__(self, weight, volume):
        self.items = Items()
        self.resources = Resources(weight, volume)

    def __repr__(self):
        return f"points:{self.get_points()}\n{self.items}"

    def get_points(self):
        return self.items.get_total_points()
    
    def add_item(self, item: Item):
        if self.resources.update_resources(item):
            self.items.add_item(item)
            return True
        else: 
            return False
    
    def save(self, knapsack_file):
        with open(knapsack_file, 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file) 
            csv_writer.writerow([f"points:{self.get_points()}"])

            for item in self.items.get_items():
                csv_writer.writerow([item])
    
    def has_room_for_item(self, item: Item):
        return self.resources.has_enough_resources(item)
    
    def get_remaining_weight(self):
        return self.resources.get_remaining_weight()
    
    def get_remaining_volume(self):
        return self.resources.get_remaining_volume()
    

class Solver_Random:

    def __init__(self, frequency):
        self.frequency = frequency
        self.best_knapsack = None 
    
    def solve(self, knapsack: Knapsack, items: Items):
        self.best_knapsack = knapsack

        for _ in range(self.frequency):
            new_knapsack = knapsack
            i_used = set()

            while True:
                random_number = random.randint(0, len(items.get_items()) - 1)
                
                if random_number in i_used:
                    continue

                item = items.get_item_on_index(random_number)

                if not new_knapsack.add_item(item):
                    break

                i_used.add(random_number)

            if new_knapsack.get_points() >= self.best_knapsack.get_points():
                self.best_knapsack = new_knapsack

    def get_best_knapsack(self):
        return self.best_knapsack


class Solver_Optimal_Recursive:

    def __init__(self):
        self.best_knapsack = None
    
def load_knapsack(knapsack_file):
    items = Items()

    with open(knapsack_file) as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for line in csv_reader:
            name = line[0]
            points = int(line[1])
            weight = int(line[2])
            volume = int(line[3])

            if name.lower() == "knapsack":
                knapsack = Knapsack(weight, volume)
            else: 
                item = Item(name, points, weight, volume)
                items.add_item(item)
    
    return knapsack, items 
                        

def main():
    # solver_random = Solver_Random(1000)
    solver_optimal_recursive = Solver_Optimal_Recursive()
    # solver_optimal_iterative_deepcopy = Solver_Optimal_Iterative_Deepcopy()
    # solver_optimal_iterative = Solver_Optimal_Iterative()
    # solver_random_improved = Solver_Random_Improved(5000)

    knapsack_file = "opdracht_knapsack\\knapsack_small"
    print("=== solving:", knapsack_file)
    # solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    # solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
    #       knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    # solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    # solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    # knapsack_file = "knapsack_medium"
    # print("=== solving:", knapsack_file)
    # solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    # solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    # solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
    #       knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    # solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    # solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    # knapsack_file = "knapsack_large"
    # print("=== solving:", knapsack_file)
    # solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    # solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")


def solve(solver, knapsack_file, solution_file):
    """ Uses 'solver' to solve the knapsack problem in file
    'knapsack_file' and writes the best solution to 'solution_file'.
    """
    knapsack, items = load_knapsack(knapsack_file)
    solver.solve(knapsack, items)
    knapsack = solver.get_best_knapsack()
    print(f"saving solution with {knapsack.get_points()} points to '{solution_file}'")
    knapsack.save(solution_file)


if __name__ == "__main__": # keep this at the bottom of the file
    main()
