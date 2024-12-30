from collections import deque

def solve():
    # Dimensions of the memory space
    MAX_X = 70
    MAX_Y = 70
    SIZE = MAX_X + 1  # 71
    
    # Number of bytes to simulate
    N = 1024
    
    # Initialize the grid: False means not corrupted (safe), True means corrupted
    grid = [[False]*SIZE for _ in range(SIZE)]
    
    # Read input for the first 1024 bytes (or less/more as needed)
    # Depending on the problem setup, you might need to read from stdin until you have 1024 lines.
    # Here we assume we have a loop that reads 1024 lines of coordinates.
    falling_coordinates = []
    for _ in range(N):
        line = input().strip()
        if not line:
            break
        x_str, y_str = line.split(',')
        x, y = int(x_str), int(y_str)
        falling_coordinates.append((x, y))
    
    # Mark corrupted cells
    for (x, y) in falling_coordinates:
        if 0 <= x <= MAX_X and 0 <= y <= MAX_Y:
            grid[y][x] = True
    
    # BFS to find shortest path from (0,0) to (70,70)
    start = (0,0)
    goal = (MAX_X, MAX_Y)
    
    # If start or goal is corrupted, no path is possible
    if grid[0][0] or grid[MAX_Y][MAX_X]:
        print("No path possible")
        return
    
    # Directions: up, down, left, right
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    
    visited = [[False]*SIZE for _ in range(SIZE)]
    visited[0][0] = True
    queue = deque()
    queue.append((0,0,0))  # (x, y, distance)
    
    while queue:
        x, y, dist = queue.popleft()
        if (x, y) == goal:
            print(dist)
            return
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= MAX_X and 0 <= ny <= MAX_Y:
                if not grid[ny][nx] and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny, dist+1))
    
    # If we reach here, no path was found
    print("No path possible")


if __name__ == "__main__":
    solve()
