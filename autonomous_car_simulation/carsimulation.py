from simulation import Simulation
from car import Car


def create_simulation() -> Simulation:
    """
    Creates the simulation using the User's Input

    """

    while True:
        print(
            "Please enter the width and height of the simulation field in x y format: "
        )

        # enter the try to get the input
        try:
            input_string: list[str] = input().strip().split()

            if len(input_string) != 2:
                print(
                    "Please provide exactly 2 numbers for the width and the height of the grid"
                )
                continue

            width, height = map(int, input_string)

            if width <= 0 or height <= 0:
                print("Width and height must be positive integers.")
                continue

            # Initialize the simulation
            print(f"You have created a field of {width} x {height}.")
            return Simulation(width, height)

        except:
            print(
                "Invalid input. Please enter two positive integers separated by a space."
            )


def main_menu_selection() -> str:
    """
    Prints the Main Menu for User Input returns the input

    """
    print("Please choose from the following options:")
    print("[1] Add a car to field")
    print("[2] Run simulation")

    return input().strip()


def main():

    print("""Welcome to Auto Driving Car Simulation!""")

    # Program Loop
    while True:
        simulation = create_simulation()

        # Simulation Menu Loop
        while True:
            if simulation.cars:
                simulation.display_current_cars()

            program_selection = main_menu_selection()

            if program_selection == "1":
                simulation.add_car()

            # Run Simulation Prompt
            elif program_selection == "2":

                # If there are no cars go back to selection
                if not simulation.cars:
                    print("No cars to simulate. Please add at least 1 car to simulate.")
                    continue

                simulation.run_simulation()
                choice = simulation.display_restart_menu()

                if choice == "1":
                    break

                return


if __name__ == "__main__":
    main()
