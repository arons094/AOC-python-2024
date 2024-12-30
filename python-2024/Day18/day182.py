from collections import deque
import sys

def is_path_possible(grid, MAX_X=70, MAX_Y=70):
    """Check if there's a path from (0,0) to (MAX_X,MAX_Y) using BFS."""
    if grid[0][0] or grid[MAX_Y][MAX_X]:
        return False
    
    SIZE = MAX_X + 1
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    visited = [[False]*SIZE for _ in range(SIZE)]
    visited[0][0] = True
    
    queue = deque([(0,0)])
    while queue:
        x, y = queue.popleft()
        if (x, y) == (MAX_X, MAX_Y):
            return True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= MAX_X and 0 <= ny <= MAX_Y:
                if not grid[ny][nx] and not visited[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    return False

def solve():
    MAX_X = 70
    MAX_Y = 70
    SIZE = MAX_X + 1
    
    # Initialize grid
    grid = [[False]*SIZE for _ in range(SIZE)]
    
    # Read all lines from stdin until none remain
    lines = sys.stdin.read().strip().split('\n')
    
    # Process each byte and check path
    for line in lines:
        if not line.strip():
            continue
        x_str, y_str = line.split(',')
        x, y = int(x_str), int(y_str)
        
        # Mark corrupted
        if 0 <= x <= MAX_X and 0 <= y <= MAX_Y:
            grid[y][x] = True
        
        # Check path
        if not is_path_possible(grid, MAX_X, MAX_Y):
            print(f"{x},{y}")
            return
    
    # If we processed all bytes and never blocked the path:
    print("No blocking byte found")

if __name__ == "__main__":
    solve()
