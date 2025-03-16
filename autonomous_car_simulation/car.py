class Car:

    VALID_DIRECTIONS = ["N", "S", "E", "W"]
    VALID_COMMANDS = ["F", "L", "R"]

    def __init__(self, x: int, y: int, direction: str, name: str, commands: str):
        """
        Initialize a car with position, direction, name and movement commands.

        Args:
                x: Initial x-coordinate (column)
                y: Initial y-coordinate (row)
                direction: Direction the car is facing (N, S, E, W)
                name: Car Name
                commands: String of commands (F, L, R) to be executed
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.name = name
        self.commands = commands
        self.collided = False
        self.collided_with = []
        # to keep track for later prints
        self.collision_position = None
        self.collision_step = None

    def move(self, command: str, width: int, height: int) -> None:
        """
        Takes a command and the width and height of the grid then executes the move on the car if possible.

        Args:
                width: Width of Simulation Grid
                height: Height of Simulation Grid
                command: (F, L, R) to be executed
        """

        # Do not move if collided
        if self.collided:
            return

        new_x = self.x
        new_y = self.y
        new_direction = self.direction

        if command == "F":

            if self.direction == "N":
                new_y = self.y + 1
            elif self.direction == "S":
                new_y = self.y - 1
            elif self.direction == "E":
                new_x = self.x + 1
            else:
                new_x = self.x - 1

        elif command == "R":

            if self.direction == "N":
                new_direction = "E"

            elif self.direction == "S":
                new_direction = "W"
            elif self.direction == "E":
                new_direction = "S"
            else:
                new_direction = "N"

        else:
            if self.direction == "N":
                new_direction = "W"

            elif self.direction == "S":
                new_direction = "E"
            elif self.direction == "E":
                new_direction = "N"
            else:
                new_direction = "S"

        if 0 <= new_x < width:
            self.x = new_x
        if 0 <= new_y < height:
            self.y = new_y
        self.direction = new_direction

    def __str__(self) -> str:
        """
        string output for car

        """
        return f"- {self.name}, ({self.x},{self.y}), {self.direction} , {self.commands}"
