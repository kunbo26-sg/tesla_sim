from car import Car


class Simulation:
    def __init__(self, width: int, height: int) -> None:
        """
        Simulation will have a grid object, and contain one or more cars
        """
        self.width = width
        self.height = height
        self.cars = []

    def add_car(self) -> None:
        """
        Adds a car to the simulation if valid
        """

        # Loop to add a valid car_name
        while True:

            print("Please enter the name of the car:")
            car_name = input().strip()

            # check for duplicates
            if any(car.name == car_name for car in self.cars):
                print("A car with that name already exists")
                continue

            # check for empty name
            if not car_name:
                print("Car name cannot be empty.")
                continue

            break

        # Loop to verify the initial coordinates are valid
        while True:
            print(
                f"Please enter initial position of car {car_name} in x y Direction format:"
            )
            pos_input = input().strip().split()

            if len(pos_input) != 3:
                print("Please provide exactly 3 values: x, y and direction")
                continue

            x_str, y_str, direction = pos_input

            try:
                x, y = int(x_str), int(y_str)

            except ValueError:
                print("x and y must both be integers")
                continue

            # Check existing cars if anything occupies the same spot
            for car in self.cars:
                if car.x == x and car.y == y:
                    print(f"The location ({x},{y}) is already occupied by another car.")
                    continue

            if not (0 <= x < self.width and 0 <= y < self.height):
                print(
                    f"The location of the car is out of bounds. The grid size is up to ({self.width-1},{self.height-1})"
                )
                continue

            if direction.upper() not in Car.VALID_DIRECTIONS:
                print(
                    f"Invalid car direction.Please note that only N, S, W, E (representing North, South, West, East) are allowed for direction."
                )
                continue

            break

        # loop for valid commands
        while True:
            print(f"Please enter the commands for car {car_name}:")

            commands = input().strip().upper()

            if not all(cmd in Car.VALID_COMMANDS for cmd in commands):
                print(
                    f"Invalid Commands, Please only supply commands from {Car.VALID_COMMANDS}. The format should be `FRL` for example."
                )
                continue
            break

        car = Car(x, y, direction.upper(), car_name, commands)
        # Add the car to the simulation
        self.cars.append(car)

    def display_current_cars(self) -> None:
        """
        Prints the list of cars in the current simulation

        """

        print("Your current list of cars are:")
        for car in self.cars:
            print(str(car))

    def display_restart_menu(self) -> str:
        """
        Prints the Menu shown to users after the simulation is run

        """

        # Menu Loop
        while True:

            print("Please choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")

            restart_choice = input().strip()

            if restart_choice == "1":
                break
            elif restart_choice == "2":
                print("Thanks for running the simulation. Goodbye!")
                break
            else:
                print("Invalid Choice. Please enter 1 or 2")
                continue

        return restart_choice

    def run_simulation(self):
        """
        Runs the simulation and outputs the results

        """
        if not self.cars:
            return

        # get the longest_command from all cars to loop though
        max_moves = max(len(car.commands) for car in self.cars)

        # Start at 1 for the display
        for move in range(1, max_moves + 1):

            for car in self.cars:
                if move <= len(car.commands) and car.collided != True:
                    command = car.commands[move - 1]
                    car.move(command, self.width, self.height)

            pos_dict = {}

            for car in self.cars:
                pos = (car.x, car.y)
                pos_dict.setdefault(pos, []).append(car)

            for pos, car_list in pos_dict.items():
                # Collision if more than one car at position
                if len(car_list) > 1:
                    for car in car_list:
                        if not car.collided:
                            car.collided = True
                            car.collided_with = [c.name for c in car_list if c != car]
                            car.collision_position = pos
                            car.collision_step = move

        # Display results
        print("After simulation, the result is:")
        for car in self.cars:
            if car.collided:
                collided_with_str = " and ".join(car.collided_with)
                pos_str = f"({car.collision_position[0]},{car.collision_position[1]})"
                print(
                    f"- {car.name}, collides with {collided_with_str} at {pos_str} at step {car.collision_step}"
                )
            else:
                pos_str = f"({car.x},{car.y})"
                print(f"- {car.name}, {pos_str} {car.direction}")
