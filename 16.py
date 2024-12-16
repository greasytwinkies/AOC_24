# reindeer starts at S facing EAST
# needs to find a path to endpoint E that gives the lowest score
# every step incurs one point, while every change in direction gives 1000 points

# we can convert the grid into a graph
# use DFS/recursion + backtracking to find the most efficient path
# base case: when the current node is the end node
# we must keep a list of visited nodes
# normal case: call the function on each of the neighboring nodes if they are not yet visited
# maintain a tracker for the score
# we also need to update the score accordingly, so must maintain a tracker for the direction of the reindeer                    


class Maze:
    def __init__(self, grid: list):
        self.grid = grid
        self.best_score = float('inf')
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                if col == "S":
                    self.start = (row_idx, col_idx)
                elif col == "E":
                    self.end = (row_idx, col_idx)

    def getNeighboringTiles(self, tile: tuple):
        # ignore tiles that are walls or out of bounds
        row_lim = len(self.grid)
        col_lim = len(self.grid[0])
        (row, col) = tile
        valid_tiles = set()
        nb = [(row+1, col), (row-1, col), (row, col-1), (row, col+1)]
        for (r, c) in nb:
            # check if out of bounds or wall
            if 0 <= r <= row_lim-1 and 0 <= c <= col_lim-1 and self.grid[r][c] != "#":
                valid_tiles.add((r,c))
        
        return valid_tiles
            


    def convert_grid_to_graph(self):
        graph = dict()
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                if col != "#":
                    tile = (row_idx, col_idx)
                    # get the coords of surrounding points that are not #
                    if neighbors := self.getNeighboringTiles(tile):
                        graph[tile] = neighbors

        self.graph = graph


    def displayGrid(self, visited: set):
        for row_idx, row in enumerate(self.grid):
            print_row = []
            for col_idx, col in enumerate(row):
                tile = (row_idx, col_idx)
                # check if it is in visited
                if tile in visited:
                    print_row.append("X")
                elif tile == self.start:
                    print_row.append("S")
                elif tile == self.end:
                    print_row.append("E")
                else:
                    print_row.append(col)
            print(*print_row, sep=' ')

    
    
    def DFS(self, visited: set, score: int, direction: str, curr: tuple, end: tuple, memo: dict):
        def checkNeighboringTile(curr: tuple, nb: tuple, direction: str):
            (curr_row, curr_col) = curr
            (nb_row, nb_col) = nb
            if direction == "N": # row - 1
                en_route = nb == (curr_row-1, curr_col)
            elif direction == "E": # col + 1
                en_route = nb == (curr_row, curr_col+1)
            elif direction == "S": # row + 1
                en_route = nb == (curr_row +1, curr_col)
            elif direction == "W": # col - 1
                en_route = nb == (curr_row, curr_col-1)

            if en_route:
                return en_route
            # return new direction
            else:
                if (nb_row, nb_col) == (curr_row-1, curr_col):
                    return "N"
                elif (nb_row, nb_col) == (curr_row, curr_col+1):
                    return "E"
                elif (nb_row, nb_col) == (curr_row+1, curr_col):
                    return "S"
                elif (nb_row, nb_col) == (curr_row, curr_col-1):
                    return "W"
                
        # terminate if score is larger than best score
        state_key = (curr, direction, frozenset(visited))
        # return cached result
        if state_key in memo:
            return memo[state_key]
        if score >= self.best_score:
            return float('inf')
        # base case: when current node == end node
        if curr == end:
            self.best_score = min(self.best_score, score)
            # store the result
            memo[state_key] = score
            return score
        else:
            # get neighbors of current node if they are not already visited
            nb = self.graph[curr]
            nb = [tile for tile in nb if tile not in visited]
            # if no more unvisited nodes, return infinitely high score
            if not nb:
                memo[state_key] = float('inf')
                return float('inf')
            # if there are still unvisited nodes, queue them and update scores accordingly
            # return the score for the path that gives the lowest score
            else:
                scores = []
                for tile in nb:
                    # check if new tile requires reindeer to change direction
                    en_route = checkNeighboringTile(curr, tile, direction)
                    visited.add(tile)
                    if en_route == True:
                        scores.append(self.DFS(visited, score+1, direction, tile, end, memo))
                    else: # change of direction, we also need to update the direction in the function call
                        new_dir = en_route
                        scores.append(self.DFS(visited, score+1001, new_dir, tile, end, memo))
                    visited.remove(tile)
                # return the lowest score
                memo[state_key] = min(scores)
                return min(scores)
    def DFS(self, visited: set, score: int, direction: str, curr: tuple, end: tuple, memo: dict):
        def checkNeighboringTile(curr: tuple, nb: tuple, direction: str):
            (curr_row, curr_col) = curr
            (nb_row, nb_col) = nb
            if direction == "N": # row - 1
                en_route = nb == (curr_row-1, curr_col)
            elif direction == "E": # col + 1
                en_route = nb == (curr_row, curr_col+1)
            elif direction == "S": # row + 1
                en_route = nb == (curr_row +1, curr_col)
            elif direction == "W": # col - 1
                en_route = nb == (curr_row, curr_col-1)

            if en_route:
                return en_route
            # return new direction
            else:
                if (nb_row, nb_col) == (curr_row-1, curr_col):
                    return "N"
                elif (nb_row, nb_col) == (curr_row, curr_col+1):
                    return "E"
                elif (nb_row, nb_col) == (curr_row+1, curr_col):
                    return "S"
                elif (nb_row, nb_col) == (curr_row, curr_col-1):
                    return "W"
                
        # terminate if score is larger than best score
        state_key = (curr, direction, frozenset(visited))
        # return cached result
        if state_key in memo:
            return memo[state_key]
        if score >= self.best_score:
            return float('inf')
        # base case: when current node == end node
        if curr == end:
            self.best_score = min(self.best_score, score)
            # store the result
            memo[state_key] = score
            return score
        else:
            # get neighbors of current node if they are not already visited
            nb = self.graph[curr]
            nb = [tile for tile in nb if tile not in visited]
            # if no more unvisited nodes, return infinitely high score
            if not nb:
                memo[state_key] = float('inf')
                return float('inf')
            # if there are still unvisited nodes, queue them and update scores accordingly
            # return the score for the path that gives the lowest score
            else:
                scores = []
                for tile in nb:
                    # check if new tile requires reindeer to change direction
                    en_route = checkNeighboringTile(curr, tile, direction)
                    visited.add(tile)
                    if en_route == True:
                        scores.append(self.DFS(visited, score+1, direction, tile, end, memo))
                    else: # change of direction, we also need to update the direction in the function call
                        new_dir = en_route
                        scores.append(self.DFS(visited, score+1001, new_dir, tile, end, memo))
                    visited.remove(tile)
                # return the lowest score
                memo[state_key] = min(scores)
                return min(scores)
    def DFS(self, visited: set, score: int, direction: str, curr: tuple, end: tuple, memo: dict):
        def checkNeighboringTile(curr: tuple, nb: tuple, direction: str):
            (curr_row, curr_col) = curr
            (nb_row, nb_col) = nb
            if direction == "N": # row - 1
                en_route = nb == (curr_row-1, curr_col)
            elif direction == "E": # col + 1
                en_route = nb == (curr_row, curr_col+1)
            elif direction == "S": # row + 1
                en_route = nb == (curr_row +1, curr_col)
            elif direction == "W": # col - 1
                en_route = nb == (curr_row, curr_col-1)

            if en_route:
                return en_route
            # return new direction
            else:
                if (nb_row, nb_col) == (curr_row-1, curr_col):
                    return "N"
                elif (nb_row, nb_col) == (curr_row, curr_col+1):
                    return "E"
                elif (nb_row, nb_col) == (curr_row+1, curr_col):
                    return "S"
                elif (nb_row, nb_col) == (curr_row, curr_col-1):
                    return "W"
                
        # terminate if score is larger than best score
        state_key = (curr, direction, frozenset(visited))
        # return cached result
        if state_key in memo:
            return memo[state_key]
        if score >= self.best_score:
            return float('inf')
        # base case: when current node == end node
        if curr == end:
            self.best_score = min(self.best_score, score)
            # store the result
            memo[state_key] = score
            return score
        else:
            # get neighbors of current node if they are not already visited
            nb = self.graph[curr]
            nb = [tile for tile in nb if tile not in visited]
            # if no more unvisited nodes, return infinitely high score
            if not nb:
                memo[state_key] = float('inf')
                return float('inf')
            # if there are still unvisited nodes, queue them and update scores accordingly
            # return the score for the path that gives the lowest score
            else:
                scores = []
                for tile in nb:
                    # check if new tile requires reindeer to change direction
                    en_route = checkNeighboringTile(curr, tile, direction)
                    visited.add(tile)
                    if en_route == True:
                        scores.append(self.DFS(visited, score+1, direction, tile, end, memo))
                    else: # change of direction, we also need to update the direction in the function call
                        new_dir = en_route
                        scores.append(self.DFS(visited, score+1001, new_dir, tile, end, memo))
                    visited.remove(tile)
                # return the lowest score
                memo[state_key] = min(scores)
                return min(scores)
            
    def DFS_iterative(self):
        stack = [(self.start, "E", 0, set())]  # (current position, direction, current score, visited set)
        memo = {}
        
        def checkNeighboringTile(curr: tuple, nb: tuple, direction: str):
            (curr_row, curr_col) = curr
            (nb_row, nb_col) = nb
            if direction == "N":  # row - 1
                en_route = nb == (curr_row - 1, curr_col)
            elif direction == "E":  # col + 1
                en_route = nb == (curr_row, curr_col + 1)
            elif direction == "S":  # row + 1
                en_route = nb == (curr_row + 1, curr_col)
            elif direction == "W":  # col - 1
                en_route = nb == (curr_row, curr_col - 1)
            
            if en_route:
                return en_route
            else:
                if (nb_row, nb_col) == (curr_row - 1, curr_col):
                    return "N"
                elif (nb_row, nb_col) == (curr_row, curr_col + 1):
                    return "E"
                elif (nb_row, nb_col) == (curr_row + 1, curr_col):
                    return "S"
                elif (nb_row, nb_col) == (curr_row, curr_col - 1):
                    return "W"

        while stack:
            curr, direction, score, visited = stack.pop()
            state_key = (curr, direction, frozenset(visited))
            
            # Skip processing if we have seen this state or score exceeds best
            if state_key in memo or score >= self.best_score:
                continue
            
            # Mark as visited in memoization
            memo[state_key] = score
            
            # If we reached the end node, update the best score
            if curr == self.end:
                self.best_score = min(self.best_score, score)
                continue
            
            # Get neighbors and check direction changes
            for nb in self.graph[curr]:
                if nb not in visited:
                    en_route = checkNeighboringTile(curr, nb, direction)
                    new_visited = visited | {nb}  # Add current node to visited
                    
                    if en_route is True:
                        stack.append((nb, direction, score + 1, new_visited))
                    else:
                        new_dir = en_route
                        stack.append((nb, new_dir, score + 1001, new_visited))
        
        return self.best_score



with open('data/input/16.txt', 'r', encoding='utf-8') as f:
    file = f.read().splitlines()

grid = [[item for item in line] for line in file]
maze = Maze(grid)
# print(maze.start, maze.end)
maze.convert_grid_to_graph()
# print(maze.graph)
# print(maze.DFS(set(maze.start), 0, "E", maze.start, maze.end, dict()))
print(maze.DFS_iterative())