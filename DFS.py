import serial
import time

# Establish serial connection to Arduino (adjust COM port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

# Constants
WALL_THRESHOLD = 15  # Distance threshold to detect walls (in cm)
GRID_SIZE = 3  # 3x3 grid

# Movement Commands
def move_forward():
    """Move the robot forward one cell"""
    ser.write(b'F')
    time.sleep(1)  # Wait for movement to complete

def turn_left():
    """Turn the robot 90 degrees left"""
    ser.write(b'L')
    time.sleep(1)

def turn_right():
    """Turn the robot 90 degrees right"""
    ser.write(b'R')
    time.sleep(1)

def stop():
    """Stop the robot"""
    ser.write(b'S')
    time.sleep(0.2)

def get_distance():
    """Get distance reading from the sensor in centimeters"""
    ser.write(b'D')
    line = ser.readline().decode().strip()
    try:
        return int(line)
    except ValueError:
        return None

# Initialize maze state
start = (0, 2)  # Starting position (x, y)
end = (2, 0)    # Exit position (x, y)
visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Track visited cells

def solve_maze(x, y, direction):
    """
    Recursive backtracking algorithm to solve the maze.
    Requirements:
    1. Attempts all valid moves from current cell
    2. Detects and avoids walls/out-of-bounds
    3. Marks visited paths to avoid revisiting
    4. Backtracks when hitting dead end
    5. Stops when exit is found
    
    Parameters:
    - x, y: current position
    - direction: current facing direction (0=North, 1=East, 2=South, 3=West)
    Returns:
    - True if path to exit is found, False otherwise
    """
    # Requirement 5: Stop when exit is found
    if (x, y) == end:
        print(f"Found exit at ({x}, {y})!")
        return True

    # Requirement 3: Mark visited paths
    visited[y][x] = True
    print(f"Visiting cell ({x}, {y})")

    # Requirement 1: Try all valid moves
    for _ in range(4):
        # Requirement 2: Detect walls
        distance = get_distance()
        if distance is not None and distance >= WALL_THRESHOLD:
            # Calculate next position based on current direction
            if direction == 0:  # North
                next_x, next_y = x, y-1
            elif direction == 1:  # East
                next_x, next_y = x+1, y
            elif direction == 2:  # South
                next_x, next_y = x, y+1
            else:  # West
                next_x, next_y = x-1, y

            # Requirement 2: Check for out-of-bounds and visited cells
            if 0 <= next_x < GRID_SIZE and 0 <= next_y < GRID_SIZE and not visited[next_y][next_x]:
                # Move forward to next cell
                move_forward()
                print(f"Moving to ({next_x}, {next_y})")

                # Recursively try to solve from next position
                if solve_maze(next_x, next_y, direction):
                    return True

                # Requirement 4: Backtrack when hitting dead end
                print(f"Backtracking from ({next_x}, {next_y}) to ({x}, {y})")
                # Turn around
                turn_left()
                turn_left()
                # Move back to previous cell
                move_forward()
                # Turn back to original direction
                turn_left()
                turn_left()

        # Try next direction
        turn_right()
        direction = (direction + 1) % 4

    # If we've tried all directions and none worked, return False
    return False

def main():
    """Main function to start the maze solving process"""
    print("Starting maze solver")
    print(f"Starting at position {start}")
    print(f"Looking for exit at {end}")
    
    # Start facing North (direction 0)
    if solve_maze(start[0], start[1], 0):
        print("Successfully found path to exit!")
    else:
        print("No path to exit found!")
    
    stop()
    print("Maze solving complete")

if __name__ == "__main__":
    main()