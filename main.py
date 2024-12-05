import os
import curses
import importlib.util
import threading
import time
import io
import contextlib

# Memoization cache
solution_cache = {}

def get_years_and_days(solutions_folder):
    years = {}
    for year in os.listdir(solutions_folder):
        year_path = os.path.join(solutions_folder, year)
        if os.path.isdir(year_path):
            days = {}
            for day_folder in os.listdir(year_path):
                day_path = os.path.join(year_path, day_folder)
                if os.path.isdir(day_path):
                    day = day_folder.split(" ")[1]  # Get day number
                    days[day] = []
                    for file in os.listdir(day_path):
                        if file.endswith(".py"):
                            day_part = file.split(".")[0]  # Remove .py
                            if day_part.startswith("d") and "p" in day_part:
                                part = day_part.split("p")[1]  # Get part number
                                if part not in days[day]:
                                    days[day].append(part)
            if days:
                years[year] = days
    return years

def display_menu(stdscr, options, title="Select an option"):
    curses.curs_set(0)  # Hide cursor
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.color_pair(2))  # Title in light purple

        # Add space after the title
        y_offset = 2  # Start adding options below the title with a space
        
        for idx, option in enumerate(options):
            x = "[x] " if idx == current_row else "[ ] "  # Highlight current selection
            line = x + option["label"]
            stdscr.addstr(y_offset + idx, 0, line)
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))  # Active option in purple
                stdscr.addstr(y_offset + idx, 0, line)
                stdscr.attroff(curses.color_pair(1))

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == ord("\n"):  # Enter key
            return options[current_row]["label"]

def run_solution(year, day, part, solutions_folder, stdscr):
    script_name = f"d{day}p{part}.py"
    script_path = os.path.join(solutions_folder, year, f"Day {day}", script_name)

    if not os.path.exists(script_path):
        stdscr.addstr(0, 0, f"Solution file {script_name} not found.", curses.color_pair(3))  # Error in red
        stdscr.addstr(1, 0, "Press any key to exit.")
        stdscr.getch()
        return

    # Prepare to capture the output
    spec = importlib.util.spec_from_file_location("solution", script_path)
    module = importlib.util.module_from_spec(spec)

    output = []

    def execute_solution():
        nonlocal output
        try:
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                    module.main()  # Execute the main function
                    output.append(buf.getvalue().strip())
        except Exception as e:
            output.append(f"Error while executing {script_name}: {e}")

    thread = threading.Thread(target=execute_solution)
    thread.start()

    loading_message = "Loading..."
    bar_length = 30
    for i in range(bar_length + 1):
        if thread.is_alive():
            stdscr.clear()
            stdscr.addstr(0, 0, f"Running solution for Year {year}, Day {day}, Part {part}...\n", curses.color_pair(2))
            stdscr.addstr(1, 0, "")  # Blank line for spacing
            stdscr.addstr(2, 0, loading_message)
            bar = "#" * i + "-" * (bar_length - i)
            stdscr.addstr(3, 0, f"[{bar}] {i * 100 // bar_length}%", curses.color_pair(2))
            stdscr.refresh()
            time.sleep(0.1)
        else:
            break

    thread.join()

    stdscr.clear()
    stdscr.addstr(0, 0, f"Running solution for Year {year}, Day {day}, Part {part}...\n", curses.color_pair(2))
    
    stdscr.addstr(1, 0, "")  # Blank line for spacing
    stdscr.addstr(2, 0, "======SOLUTION======", curses.color_pair(1))  # "======SOLUTION======" in purple
    
    stdscr.addstr(3, 0, "")  # Blank line for spacing
    stdscr.addstr(4, 0, output[0] if output else f"{script_name} executed, but no output was returned.", curses.color_pair(4))  # Normal output in white
    stdscr.addstr(5, 0, "") # Blank line for spacing
    stdscr.addstr(6, 0, f"Press any key to exit.", curses.color_pair(2))  # "Press any key to exit." in green
    stdscr.getch()

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Active options in purple
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Title and loading
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Errors
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text

    solutions_folder = "./solutions"
    years = get_years_and_days(solutions_folder)

    # Step 1: Select a year
    year_options = [{"label": f"Year {year}", "selected": False} for year in sorted(years.keys())]
    year_options.append({"label": "Quit", "selected": False})  # Add Quit option
    while True:
        selected_year = display_menu(stdscr, year_options, title="Select a Year")
        
        if selected_year == "Quit":
            break  # Exit the program

        year = selected_year.split(" ")[1]  # Extract year

        while True:
            # Step 2: Select a day
            day_options = [{"label": f"Day {day}", "selected": False} for day in sorted(years[year].keys())]
            day_options.append({"label": "Go Back", "selected": False})  # Add Go Back option
            day_options.append({"label": "Quit", "selected": False})  # Add Quit option
            selected_day = display_menu(stdscr, day_options, title=f"Select a Day for Year {year}")
            
            if selected_day == "Go Back":
                break  # Exit the day selection loop to go back to year selection
            elif selected_day == "Quit":
                return  # Exit the program
            
            day = selected_day.split(" ")[1]  # Extract day number

            while True:
                # Step 3: Select a part
                parts = sorted(years[year][day])
                part_options = [{"label": f"Part {part}", "selected": False} for part in parts]
                part_options.append({"label": "Go Back", "selected": False})  # Add Go Back option
                part_options.append({"label": "Quit", "selected": False})  # Add Quit option
                selected_part = display_menu(stdscr, part_options, title=f"Select a Part for Day {day} in Year {year}")
                
                if selected_part == "Go Back":
                    break  # Exit the part selection loop to go back to day selection
                elif selected_part == "Quit":
                    return  # Exit the program
                
                part = selected_part.split(" ")[1]  # Extract part number

                # Step 4: Run solution
                stdscr.clear()
                run_solution(year, day, part, solutions_folder, stdscr)

if __name__ == "__main__":
    curses.wrapper(main)
