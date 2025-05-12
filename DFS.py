import serial
import time

# Establish serial connection to Arduino (adjust COM port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

# Constants
WALL_THRESHOLD = 15  # Distance threshold to detect walls (in cm)

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

def check_for_wall():
    """Check if there is a wall in front of the robot"""
    distance = get_distance()
    return distance is not None and distance < WALL_THRESHOLD

def dfs(x, y, direction, visited):
    """
    Recursive DFS with backtracking.
    Parameters:
    - x, y: current position
    - direction: current facing direction (0=North, 1=East, 2=South, 3=West)
    - visited: 2D array tracking visited cells
    """
    if (x, y) == end:
        print(f"Reached goal at ({x}, {y})")
        return True

    visited[y][x] = True  # mark current cell as visited

    # Try all possible directions (forward, right, left)
    for _ in range(4):
        # Check for wall before moving
        if not check_for_wall():
            # No wall detected, move forward
            move_forward()
            
            # Calculate next position based on current direction
            if direction == 0:  # North
                nx, ny = x, y-1
            elif direction == 1:  # East
                nx, ny = x+1, y
            elif direction == 2:  # South
                nx, ny = x, y+1
            else:  # West
                nx, ny = x-1, y
            
            if 0 <= nx < 3 and 0 <= ny < 3 and not visited[ny][nx]:
                if dfs(nx, ny, direction, visited):
                    return True
                
                # Backtrack: turn around, move back, turn around again
                turn_left()
                turn_left()
                move_forward()
                turn_left()
                turn_left()
        
        # Turn right to face the next direction
        turn_right()
        direction = (direction + 1) % 4

    return False

def main():
    print("Starting DFS navigation")
    print(f"Starting at position {start} facing direction {start_direction}")
    dfs(start[0], start[1], start_direction, visited)
    stop()
    print("Navigation complete")

if __name__ == "__main__":
    main()