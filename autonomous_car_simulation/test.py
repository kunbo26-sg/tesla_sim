from unittest.mock import patch
import pytest
from car import Car
from simulation import Simulation


class TestCar:
    def test_car_initialization(self):
        """Test initialization of Car objects"""
        car = Car(0, 0, "N", "TestCar", "FLR")

        assert car.x == 0
        assert car.y == 0
        assert car.direction == "N"
        assert car.name == "TestCar"
        assert car.commands == "FLR"
        assert car.collided is False
        assert car.collided_with == []
        assert car.collision_position is None
        assert car.collision_step is None

    def test_car_move_forward(self):
        """Test forward movement in all direction"""
        # Test moving North
        car_n = Car(5, 5, "N", "CarN", "F")
        car_n.move("F", 10, 10)
        assert car_n.x == 5
        assert car_n.y == 6

        # Test moving South
        car_s = Car(5, 5, "S", "CarS", "F")
        car_s.move("F", 10, 10)
        assert car_s.x == 5
        assert car_s.y == 4

        # Test moving East
        car_e = Car(5, 5, "E", "CarE", "F")
        car_e.move("F", 10, 10)
        assert car_e.x == 6
        assert car_e.y == 5

        # Test moving West
        car_w = Car(5, 5, "W", "CarW", "F")
        car_w.move("F", 10, 10)
        assert car_w.x == 4
        assert car_w.y == 5

    def test_car_rotate_right(self):
        """Test rotating right from all directions"""
        # North to East
        car = Car(0, 0, "N", "TestCar", "R")
        car.move("R", 10, 10)
        assert car.direction == "E"

        # East to South
        car = Car(0, 0, "E", "TestCar", "R")
        car.move("R", 10, 10)
        assert car.direction == "S"

        # South to West
        car = Car(0, 0, "S", "TestCar", "R")
        car.move("R", 10, 10)
        assert car.direction == "W"

        # West to North
        car = Car(0, 0, "W", "TestCar", "R")
        car.move("R", 10, 10)
        assert car.direction == "N"

    def test_car_rotate_left(self):
        """Test rotating left from all directions"""
        # North to West
        car = Car(0, 0, "N", "TestCar", "L")
        car.move("L", 10, 10)
        assert car.direction == "W"

        # West to South
        car = Car(0, 0, "W", "TestCar", "L")
        car.move("L", 10, 10)
        assert car.direction == "S"

        # South to East
        car = Car(0, 0, "S", "TestCar", "L")
        car.move("L", 10, 10)
        assert car.direction == "E"

        # East to North
        car = Car(0, 0, "E", "TestCar", "L")
        car.move("L", 10, 10)
        assert car.direction == "N"

    def test_boundary_constraints(self):
        """Test that cars don't move beyond grid boundaries"""
        # Try to move beyond northern boundary
        car = Car(5, 9, "N", "TestCar", "F")
        car.move("F", 10, 10)
        assert car.x == 5
        assert car.y == 9

        # Try to move beyond southern boundary
        car = Car(5, 0, "S", "TestCar", "F")
        car.move("F", 10, 10)
        assert car.x == 5
        assert car.y == 0

        # Try to move beyond eastern boundary
        car = Car(9, 5, "E", "TestCar", "F")
        car.move("F", 10, 10)
        assert car.x == 9
        assert car.y == 5

        # Try to move beyond western boundary
        car = Car(0, 5, "W", "TestCar", "F")
        car.move("F", 10, 10)
        assert car.x == 0
        assert car.y == 5

    def test_car_str_representation(self):
        """Test the string representation of a car"""
        car = Car(3, 4, "N", "TestCar", "FLR")
        expected_str = "- TestCar, (3,4), N , FLR"
        assert str(car) == expected_str


class TestSimulation:
    def test_simulation_initialization(self):
        """Test proper initialization of Simulation objects"""
        sim = Simulation(10, 10)
        assert sim.width == 10
        assert sim.height == 10
        assert sim.cars == []

    @patch("builtins.input", side_effect=["Car1", "2 3 N", "FLR"])
    def test_add_car(self, mock_input):
        """Test adding a car to the simulation"""
        sim = Simulation(10, 10)
        sim.add_car()

        assert len(sim.cars) == 1
        car = sim.cars[0]
        assert car.name == "Car1"
        assert car.x == 2
        assert car.y == 3
        assert car.direction == "N"
        assert car.commands == "FLR"

    def test_collision_detection(self):
        """Test that collisions are detected correctly"""
        sim = Simulation(10, 10)

        # Create two cars that will collide
        car1 = Car(2, 2, "N", "Car1", "FF")
        car2 = Car(2, 4, "S", "Car2", "FF")

        sim.cars = [car1, car2]
        sim.run_simulation()

        # Both cars should have collided at (2,3)
        assert car1.collided is True
        assert car2.collided is True
        assert car1.collision_position == (2, 3)
        assert car2.collision_position == (2, 3)
        assert "Car2" in car1.collided_with
        assert "Car1" in car2.collided_with

    def test_multiple_commands_execution(self):
        """Test execution of multiple commands for a car"""
        sim = Simulation(10, 10)

        car = Car(2, 2, "N", "TestCar", "FFRFF")
        sim.cars = [car]
        sim.run_simulation()

        # After the commands, the car should be at (4,4) facing East
        assert car.x == 4
        assert car.y == 4
        assert car.direction == "E"
        assert car.collided is False

    def test_cars_with_different_command_lengths(self):
        """Test simulation with cars having different command lengths"""
        sim = Simulation(10, 10)

        car1 = Car(1, 1, "N", "Car1", "F")
        car2 = Car(5, 5, "S", "Car2", "FFLRFR")

        sim.cars = [car1, car2]
        sim.run_simulation()

        # Car1
        assert car1.x == 1
        assert car1.y == 2
        assert car1.direction == "N"

        # Car2
        assert car2.x == 5
        assert car2.y == 2
        assert car2.direction == "W"
