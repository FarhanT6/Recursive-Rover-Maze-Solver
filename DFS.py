import serial
import time

# Establish serial connection to Arduino (adjust COM port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset


# Movement Commands
def move_forward():
    ser.write(b'F')
    time.sleep(1)  # Wait for movement to complete


def turn_left():
    ser.write(b'L')
    time.sleep(1)


def turn_right():
    ser.write(b'R')
    time.sleep(1)


def stop():
    ser.write(b'S')
    time.sleep(0.2)


def get_distance():
    ser.write(b'D')
    line = ser.readline().decode().strip()
    try:
        return int(line)
    except ValueError:
        return None


# Maze Grid (0 = free, 1 = wall)
grid = [
    [0, 1, 0],
    [0, 0, 0],
    [1, 1, 0]
]
start = (0, 0)
end = (2, 2)

# Placeholder for visited state
visited = [[False for _ in range(3)] for _ in range(3)]


# DFS Pathfinding Placeholder
def dfs(x, y, visited):
    """
    Recursive DFS with backtracking.
    You must:
    - Check if (x, y) is the exit.
    - Use get_distance() to detect walls before moving.
    - Use move_forward(), turn_left(), turn_right() as needed.
    - Mark visited[x][y] = True.
    - Backtrack when no moves are valid.

    TODO: Implement full DFS logic
    """
    pass


# Main Execution
def main():
    print("Starting DFS navigation")
    dfs(start[0], start[1], visited)
    stop()
    print("Navigation complete")


if __name__ == "__main__":
    main()