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
    
    def __repr__(self):
        return '\n'.join(str(item) for item in self.item_list)
    
    def __add__(self, other):
        new_items = Item()
        new_items.item_list = self.item_list + other.item_list

        return new_items

    def add_item(self, *args):
        for item in args:
            self.item_list.append(item)
    
    def get_total_points(self):
        sum = 0

        for item in self.item_list:
            sum += item.get_points()

        return sum
    
    def get_item_on_index(self, index):
        if index > len(self.item_list):
            return None 
        return self.item_list[index]


class Resources:

    def __init__(self, weight_available, volume_available):
        self.remaining_weight = weight_available
        self.remaining_volume = volume_available
    
    def update_resources(self, item):
        if item.get_weight() <= self.remaining_weight and item.get_volume() <= self.remaining_volume:
            self.remaining_weight -= item.get_weight()
            self.remaining_volume -= item.get_volume()
            return True
        else:
            return False

    def get_remaining_weight(self):
        return self.remaining_weight
    
    def get_remaining_volume(self):
        return  self.remaining_volume


class Knapsack:

    def __init__(self, weight, volume):
        self.items = Items()
        self.resources = Resources(weight, volume)
    
    def get_points(self):
        return self.items.get_total_points()
    
    def add_item(self, item: Item):
        if self.resources.update_resources(item):
            self.items.add_item(item)

            return True
        return False
    
class Solver_Random:

    def __init__(self, frequency):
        self.frequency = frequency
        self.best_knapsack = None 
    
    def solve(self, knapsack: Knapsack, items: Items):
        best_knapsack = knapsack

        for i in range(self.frequency):
            new_knapsack = knapsack
            
            while True:
                random_number = random.randint(0, len(items) - 1)
                item = items.get_item_on_index(random_number)

                if not new_knapsack.add_item(item):
                    break

            if new_knapsack.get_points > best_knapsack.get_points():
                best_knapsack = new_knapsack

    def get_best_knapsack(self):
        return self.best_knapsack

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
    solver_random = Solver_Random(1000)
    solver_optimal_recursive = Solver_Optimal_Recursive()
    solver_optimal_iterative_deepcopy = Solver_Optimal_Iterative_Deepcopy()
    solver_optimal_iterative = Solver_Optimal_Iterative()
    solver_random_improved = Solver_Random_Improved(5000)

    knapsack_file = "knapsack_small"
    print("=== solving:", knapsack_file)
    solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
          knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    knapsack_file = "knapsack_medium"
    print("=== solving:", knapsack_file)
    solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
          knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    knapsack_file = "knapsack_large"
    print("=== solving:", knapsack_file)
    solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")


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
