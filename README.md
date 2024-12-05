# My Advent of Code 2024 Journey Tracker

Welcome to my Advent of Code 2024 repository! This project tracks my progress and solutions for each day's challenges during the Advent of Code 2024. The solutions are implemented in Python and organized in a structured format for easy navigation.

## Project Structure
```shell 
├── .venv # Virtual environment for libraries 
├── .env # Contains private session token 
├── main.py # Main script to navigate and run solutions 
├── requirements.txt # Lists all dependencies 
└── solutions # Contains solution files 
    └── 2024 
        ├── Day 1 
        │   ├── d1p1.py # Solution for Day 1, Part 1 
        │   └── d1p2.py # Solution for Day 1, Part 2 
        ├── Day 2 
        │   ├── d2p1.py # Solution for Day 2, Part 1 
        │   └── d2p2.py # Solution for Day 2, Part 2 
        └── ... # Other days' solutions
```


## Features

- **Interactive Menu**: Use an interactive console interface to select the year, day, and part of the solution you want to run.
- **Curses Library**: Utilizes the `curses` library for a user-friendly navigation experience.

## Setup Instructions

To set up this project on your local machine, follow these steps:

1. **Clone the Repository**:

    ```shell
    git clone https://github.com/ZyS1b/Advent-of-Code.git

    cd Advent-of-Code
    ```

2. **Create and Activate the Virtual Environment**:
   
    ```shell 
    python -m venv .venv
    
    .\.venv\Scripts\activate
    ```

3. **Install Dependencies**:
    Make sure to install all the required libraries:

    ```shell 
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:

   Create a `.env` file in the root directory to store your private session token. Add the following line to the `.env` file:
    ```bash
    AOC_SESSION_TOKEN = your_session_token_here
    ```

    To get your session token, follow these steps:

    1. Log in to the [Advent of Code](https://adventofcode.com/) website.
    2. Open your browser's developer tools (usually accessible by pressing `F12` or right-clicking on the page and selecting "Inspect").
    3. Navigate to the "Application" tab (or "Storage" in some browsers) and look for "Cookies" in the left sidebar.
    4. Find the `session` cookie associated with the Advent of Code website. The value of this cookie is your session token.
    5. Copy the session token and paste it in the `.env` file, replacing `your_session_token_here`.

    **Important**: Ensure that the `.env` file is not shared publicly or committed to version control, as it contains sensitive information.

5. **Run the Application**:
    To start the application, simply run:
    
    ```shell
    python main.py
    ```

## Usage
Once the application is running, you'll be presented with a menu to select the year, day, and part of the solution you want to execute. Use the arrow keys to navigate through the options and press Enter to select.

## Contributing
Feel free to contribute by forking the repository and submitting a pull request with your improvements or additional solutions!

## License
This project is licensed under the MIT License - see the LICENSE file for details.