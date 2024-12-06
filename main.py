import os
import curses
import importlib.util
import threading
import time
import io
import contextlib

# Function to retrieve the available years and days from the solutions folder
def get_years_and_days(solutions_folder):
    years = {}
    for year in os.listdir(solutions_folder):  # Loop through each year folder
        year_path = os.path.join(solutions_folder, year)
        if os.path.isdir(year_path):  # Ensure it's a directory
            days = {}
            for day_folder in os.listdir(year_path):  # Loop through each day folder
                day_path = os.path.join(year_path, day_folder)
                if os.path.isdir(day_path):  # Ensure it's a directory
                    day = day_folder.split(" ")[1]  # Extract day number
                    days[day] = []
                    for file in os.listdir(day_path):  # Loop through files in the day folder
                        if file.endswith(".py"):  # Consider only Python files
                            day_part = file.split(".")[0]
                            if day_part.startswith("d") and "p" in day_part:  # Ensure proper naming
                                part = day_part.split("p")[1]
                                if part not in days[day]:
                                    days[day].append(part)
            if days:  # Only add years with valid days
                years[year] = days
    return years

# Function to display a scrolling menu
def display_menu(stdscr, options, title="Select an option"):
    curses.curs_set(0)  # Disable cursor visibility
    current_row = 0  # Currently selected row
    scroll_offset = 0  # Offset for scrolling

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()  # Get terminal dimensions
        visible_height = height - 4  # Reserve space for title and footer

        # Display the menu title
        stdscr.addstr(0, 0, title[:width], curses.color_pair(2))

        # Display visible menu items based on scrolling offset
        visible_options = options[scroll_offset : scroll_offset + visible_height]
        for idx, option in enumerate(visible_options):
            line_number = idx + 2  # Adjust for title spacing
            if scroll_offset + idx == current_row:  # Highlight the selected row
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(line_number, 0, f"> {option['label'][:width-2]}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(line_number, 0, f"  {option['label'][:width-2]}")

        # Display navigation footer
        footer = "[UP/DOWN to navigate, ENTER to select]"
        stdscr.addstr(height - 1, 0, footer[:width], curses.color_pair(4))

        stdscr.refresh()

        # Handle user input
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:  # Move up
            current_row -= 1
            if current_row < scroll_offset:  # Adjust scroll if needed
                scroll_offset -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:  # Move down
            current_row += 1
            if current_row >= scroll_offset + visible_height:  # Adjust scroll if needed
                scroll_offset += 1
        elif key == ord("\n"):  # Select an option
            return options[current_row]["label"]

# Function to execute the solution script for a given year, day, and part
def run_solution(year, day, part, solutions_folder, stdscr):
    script_name = f"d{day}p{part}.py"  # Construct script filename
    script_path = os.path.join(solutions_folder, year, f"Day {day}", script_name)

    if not os.path.exists(script_path):  # Check if the file exists
        stdscr.addstr(0, 0, f"Solution file {script_name} not found.", curses.color_pair(3))
        stdscr.addstr(1, 0, "Press any key to exit.")
        stdscr.getch()
        return

    spec = importlib.util.spec_from_file_location("solution", script_path)
    module = importlib.util.module_from_spec(spec)

    output = []  # Store the output from the script

    # Function to execute the script in a separate thread
    def execute_solution():
        nonlocal output
        try:
            spec.loader.exec_module(module)  # Load the module
            if hasattr(module, "main"):  # Ensure there's a main function
                with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                    module.main()  # Call the main function
                    output.append(buf.getvalue().strip())
        except Exception as e:
            output.append(f"Error while executing {script_name}: {e}")

    thread = threading.Thread(target=execute_solution)  # Run the solution in a thread
    thread.start()

    # Display a loading bar while the script is running
    loading_message = "Loading..."
    bar_length = 30
    for i in range(bar_length + 1):
        if thread.is_alive():
            stdscr.clear()
            stdscr.addstr(0, 0, f"Running solution for Year {year}, Day {day}, Part {part}...\n", curses.color_pair(2))
            stdscr.addstr(2, 0, loading_message)
            bar = "#" * i + "-" * (bar_length - i)
            stdscr.addstr(3, 0, f"[{bar}] {i * 100 // bar_length}%", curses.color_pair(2))
            stdscr.refresh()
            time.sleep(0.1)
        else:
            break

    thread.join()  # Wait for the thread to finish

    # Display the output of the script
    stdscr.clear()
    stdscr.addstr(0, 0, f"Running solution for Year {year}, Day {day}, Part {part}...\n", curses.color_pair(2))
    stdscr.addstr(2, 0, "======SOLUTION======", curses.color_pair(1))
    stdscr.addstr(4, 0, output[0] if output else f"{script_name} executed, but no output was returned.", curses.color_pair(4))
    stdscr.addstr(6, 0, "Press any key to exit.", curses.color_pair(2))
    stdscr.getch()

# Main function to handle the curses interface
def main(stdscr):
    # Initialize color pairs for different UI elements
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Highlight
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Titles and success messages
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)      # Error messages
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Footer and normal text

    solutions_folder = "./solutions"  # Folder containing solution scripts
    years = get_years_and_days(solutions_folder)

    # Create a list of years for the main menu
    year_options = [{"label": f"Year {year}", "selected": False} for year in sorted(years.keys())]
    year_options.append({"label": "Quit", "selected": False})

    while True:
        # Select a year
        selected_year = display_menu(stdscr, year_options, title="Select a Year")
        if selected_year == "Quit":
            break

        year = selected_year.split(" ")[1]  # Extract the year from the selection
        while True:
            # Create a list of days for the selected year
            day_options = [{"label": f"Day {day}", "selected": False} for day in sorted(years[year].keys())]
            day_options.append({"label": "Go Back", "selected": False})
            day_options.append({"label": "Quit", "selected": False})

            selected_day = display_menu(stdscr, day_options, title=f"Select a Day for Year {year}")
            if selected_day == "Go Back":
                break
            elif selected_day == "Quit":
                return

            day = selected_day.split(" ")[1]  # Extract the day from the selection
            while True:
                # Create a list of parts for the selected day
                parts = sorted(years[year][day])
                part_options = [{"label": f"Part {part}", "selected": False} for part in parts]
                part_options.append({"label": "Go Back", "selected": False})
                part_options.append({"label": "Quit", "selected": False})

                selected_part = display_menu(stdscr, part_options, title=f"Select a Part for Day {day} in Year {year}")
                if selected_part == "Go Back":
                    break
                elif selected_part == "Quit":
                    return

                part = selected_part.split(" ")[1]  # Extract the part from the selection
                stdscr.clear()
                run_solution(year, day, part, solutions_folder, stdscr)

# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main)
