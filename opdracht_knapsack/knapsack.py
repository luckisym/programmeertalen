import csv
import random
import copy


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

    def __init__(self, items=None):
        if items is None:
            self.item_list = []
        else:
            self.item_list = [item for item in items]

    def __len__(self):
        return len(self.item_list)

    def __getitem__(self, key):
        return self.item_list[key] if self.index_is_within_bounds(key) else None

    def add_item(self, item: Item):
        self.item_list.append(item)

    def remove_item(self, item: Item):
        if item in self.item_list:
            self.item_list.remove(item)

    def get_total_points(self):
        sum = 0

        for item in self.item_list:
            sum += item.get_points()

        return sum

    def remove_item(self, item: Item):
        if item in self.item_list:
            self.item_list.remove(item)

    def get_items(self):
        return self.item_list

    def set_items(self, items):
        self.item_list = [item for item in items]

    def index_is_within_bounds(self, index):
        return -len(self.item_list) <= index < len(self.item_list)

    def is_empty(self):
        return not self.item_list

    def contains_item(self, item: Item):
        return item in self.item_list


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
        return (
            item.get_weight() <= self.remaining_weight
            and item.get_volume() <= self.remaining_volume
        )

    def get_remaining_weight(self):
        return self.remaining_weight

    def get_remaining_volume(self):
        return self.remaining_volume


class Knapsack:

    def __init__(self, weight, volume, items=None):
        self.weight = weight
        self.volume = volume
        self.items = Items()
        self.resources = Resources(weight, volume)

        if items is not None:
            self.items.set_items(items)

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

    def remove_item(self, item: Item):
        self.items.remove_item(item)

    def save(self, knapsack_file):
        with open(knapsack_file, "w", newline="") as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow([f"points:{self.get_points()}"])

            for item in self.items.get_items():
                csv_writer.writerow([item])

    def has_room_for_item(self, item: Item):
        return self.resources.has_enough_resources(item)

    def get_max_weight(self):
        return self.weight

    def get_max_volume(self):
        return self.volume

    def get_resources(self):
        return (
            self.resources.get_remaining_weight(),
            self.resources.get_remaining_volume(),
        )

    def get_items(self):
        return self.items.get_items()

    def contains_item(self, item: Item):
        return self.items.contains_item(item)


class Solver_Random:

    def __init__(self, frequency):
        self.frequency = frequency
        self.best_knapsack = None

    def solve(self, knapsack: Knapsack, items: Items):
        self.best_knapsack = knapsack

        for _ in range(self.frequency):
            new_knapsack = Knapsack(
                knapsack.get_max_weight(), knapsack.get_max_volume()
            )
            self.shuffle_items(items)

            for item in items.get_items():
                if not new_knapsack.add_item(item):
                    break

            if new_knapsack.get_points() >= self.best_knapsack.get_points():
                self.best_knapsack = new_knapsack

    def get_best_knapsack(self):
        return self.best_knapsack

    def shuffle_items(self, items: Items):
        items_copy = items.get_items()[:]
        random.shuffle(items_copy)
        items.set_items(items_copy)


class Solver_Optimal_Recursive:

    def __init__(self):
        self.best_knapsack = None

    def solve(self, knapsack: Knapsack, items: Items):
        starting_index = len(items) - 1
        self.best_knapsack = self.solve_helper(knapsack, items, starting_index)

    def solve_helper(self, knapsack: Knapsack, items: Items, index):
        if index < 0:
            return knapsack

        item = items[index]

        remaining_w, remaining_v = knapsack.get_resources()
        current_items = knapsack.get_items()

        ks_with_item = Knapsack(remaining_w, remaining_v, current_items)
        ks_without_item = Knapsack(remaining_w, remaining_v, current_items)

        ks_with_item.add_item(item)

        return max(
            self.solve_helper(ks_with_item, items, index - 1),
            self.solve_helper(ks_without_item, items, index - 1),
            key=lambda ks: ks.get_points(),
        )

    def get_best_knapsack(self):
        return self.best_knapsack


class Solver_Optimal_Iterative_Deepcopy:

    def __init__(self):
        self.best_knapsack = None

    def solve(self, knapsack: Knapsack, items: Items):
        highest_points = 0
        best_ks = None
        starting_index = len(items) - 1
        stack = [(knapsack, starting_index)]

        while stack:
            curr_ks, curr_index = stack.pop()

            if curr_index < 0:
                if curr_ks.get_points() >= highest_points:
                    highest_points = curr_ks.get_points()
                    best_ks = curr_ks
                continue

            item = items[curr_index]

            ks_with_item = copy.deepcopy(curr_ks)
            ks_without_item = copy.deepcopy(curr_ks)

            if ks_with_item.add_item(item):
                stack.append((ks_with_item, curr_index - 1))

            stack.append((ks_without_item, curr_index - 1))

        self.best_knapsack = best_ks

    def get_best_knapsack(self):
        return self.best_knapsack


class Solver_Optimal_Iterative:

    def __init__(self):
        self.best_ks = None

    def solve(self, knapsack: Knapsack, items: Items):
        highest_points = 0
        best_ks = None
        starting_index = len(items) - 1
        stack = [(knapsack, starting_index)]

        while stack:
            curr_ks, curr_index = stack.pop()

            if curr_index < 0:
                if curr_ks.get_points() >= highest_points:
                    highest_points = curr_ks.get_points()
                    best_ks = curr_ks
                continue

            item = items[curr_index]

            ks_weight, ks_volume = curr_ks.get_resources()
            ks_items = curr_ks.get_items()

            ks_with_item = Knapsack(ks_weight, ks_volume, ks_items)
            ks_without_item = Knapsack(ks_weight, ks_volume, ks_items)

            if ks_with_item.add_item(item):
                stack.append((ks_with_item, curr_index - 1))

            stack.append((ks_without_item, curr_index - 1))

        self.best_ks = best_ks

    def get_best_knapsack(self):
        return self.best_ks


class Solver_Random_Improved:

    def __init__(self, frequency):
        self.best_ks = None
        self.frequency = frequency

    def solve(self, knapsack: Knapsack, items: Items):
        starting_ks = self.initialize_ks(knapsack, items)
        self.best_ks = starting_ks

        for _ in range(self.frequency):
            ks_items = self.best_ks.get_items()
            ks_weight, ks_volume = self.best_ks.get_resources()

            new_ks = Knapsack(ks_weight, ks_volume, ks_items)

            item = self.random_item(new_ks.get_items())
            new_ks.remove_item(item)

            while True:
                rand_item = self.random_item(items.get_items())
                if not new_ks.add_item(rand_item):
                    break

            if new_ks.get_points() > self.best_ks.get_points():
                self.best_ks = new_ks

    def get_best_knapsack(self):
        return self.best_ks

    def initialize_ks(self, knapsack: Knapsack, items):
        solver_random = Solver_Random(1)
        solver_random.solve(knapsack, items)

        return solver_random.get_best_knapsack()

    def random_item(self, options):
        random_number = random.randint(0, len(options) - 1)
        return options[random_number]


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

    # knapsack_file = "opdracht_knapsack\\knapsack_small"
    # print("=== solving:", knapsack_file)
    # solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    # solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    # solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
    #       knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    # solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    # solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    # knapsack_file = "opdracht_knapsack\\knapsack_medium"
    # print("=== solving:", knapsack_file)
    # solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    # solve(solver_optimal_recursive, knapsack_file + ".csv", knapsack_file + "_solution_optimal_recursive.csv")
    # solve(solver_optimal_iterative_deepcopy, knapsack_file + ".csv",
    #       knapsack_file + "_solution_optimal_iterative_deepcopy.csv")
    # solve(solver_optimal_iterative, knapsack_file + ".csv", knapsack_file + "_solution_optimal_iterative.csv")
    # solve(solver_random_improved, knapsack_file + ".csv", knapsack_file + "_solution_random_improved.csv")

    knapsack_file = "opdracht_knapsack\\knapsack_large"
    print("=== solving:", knapsack_file)
    solve(solver_random, knapsack_file + ".csv", knapsack_file + "_solution_random.csv")
    solve(
        solver_random_improved,
        knapsack_file + ".csv",
        knapsack_file + "_solution_random_improved.csv",
    )


def solve(solver, knapsack_file, solution_file):
    """Uses 'solver' to solve the knapsack problem in file
    'knapsack_file' and writes the best solution to 'solution_file'.
    """
    knapsack, items = load_knapsack(knapsack_file)
    solver.solve(knapsack, items)
    knapsack = solver.get_best_knapsack()
    print(f"saving solution with {knapsack.get_points()} points to '{solution_file}'")
    knapsack.save(solution_file)


if __name__ == "__main__":  # keep this at the bottom of the file
    main()
