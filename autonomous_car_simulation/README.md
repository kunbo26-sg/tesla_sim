# Auto Driving Car Simulation

This project implements a simulation for autonomous driving cars on a rectangular grid, allowing users to add cars, specify their starting positions and directions, and issue movement commands via a command-line interface (CLI). The simulation supports multiple cars, collision detection, and boundary enforcement, inspired by the provided requirements.

It does not allow for the removal of cars from the simulation (TBC)

## Features

### **Simulation Class**

- **Field Setup**: Define a rectangular grid with width and height.For a 10x10 grid, the bottom-left is (0,0) and the top-right is (9,9)

- **Cars**: Each simulation can allow fors all slots of the grid to be filled up. Cars must have different names and initial positions.

- **Collision Detection**: If two cars collide, the simulation will report the details of the collision.

- **Boundary Enforcement**: Grid ensures cars cannot move past boundaries.

### **Car Class**

- **Commands**:

  - **F**: Move forward one grid point.
  - **L**: Rotate 90° right.
  - **R**: Rotate 90° left.

## Prerequisites

- Python 3.11 or higher
- Dependencies listed in `requirements.txt` (only `pytest` for testing)

## How to Run

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd autonomous_car_simulation
   ```

2. **Run the program**:

   ```bash
   python carsimulation.py
   ```

   Follow the CLI prompts to:
   Set the field dimensions (e.g., 10 10).
   Add cars with name, position, direction (e.g., A, 1 2 N), and commands (e.g., FFRFFFFRRL).
   Run the simulation or add more cars.

3. **Run tests on functions**:

   ```bash
   pytest test.py
   ```

   This file runs the tests to ensure the Simulation and Car classes functions are handling cases correctly.

## Assumptions

1. Cars cannot occupy the same grid spot, even at the initial point

2. Sequence of execution is by order of whichever car is added to the simulation first

## Improvements

1. The script is such that it will keep prompting the user for valid inputs instead of raising exceptions and quitting.

2. It handles the case where a simulation is started without cars.

3. Car and Simulation classes are kept separate so that they can be modified separately for readability.
