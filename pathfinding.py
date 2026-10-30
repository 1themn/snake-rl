from collections import deque
import heapq

def get_neighbors(position, blocked, grid_size=20):
    x, y = position

    directions = [
        (0, -1),  # Up
        (0, 1),   # Down
        (-1, 0),  # Left
        (1, 0)    # Right
    ]

    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if (
            0 <= nx < grid_size
            and 0 <= ny < grid_size
            and (nx, ny) not in blocked
        ):
            neighbors.append((nx, ny))

    return neighbors


def bfs(start, goal, blocked, grid_size=20):
    queue = deque([start])
    visited = {start}
    came_from = {}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == goal:
            path = []

            while current != start:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path, nodes_explored

        for neighbor in get_neighbors(current, blocked, grid_size):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return [], nodes_explored


def astar(start, goal, blocked, grid_size=20):
    def heuristic(position):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    open_set = [(heuristic(start), start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    nodes_explored = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in visited:
            continue
        nodes_explored += 1

        if current == goal:
            path = []

            while current != start:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path, nodes_explored

        visited.add(current)

        for neighbor in get_neighbors(current, blocked, grid_size):
            new_g = g_score[current] + 1

            if new_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = new_g

                f_score = new_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, neighbor))

    return [], nodes_explored