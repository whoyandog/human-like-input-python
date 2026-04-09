QWERTY_GRID = [
    "`1234567890-=",
    "qwertyuiop[]\\",
    "asdfghjkl;'",
    "zxcvbnm,./",
]


def build_neighbor_map(grid=None):
    source_grid = grid or QWERTY_GRID

    pos = {}
    for row_idx, row in enumerate(source_grid):
        for col_idx, key in enumerate(row):
            pos[key] = (row_idx, col_idx)

    neighbors = {}
    for key, (row_idx, col_idx) in pos.items():
        points = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr = row_idx + dr
                nc = col_idx + dc
                if 0 <= nr < len(source_grid):
                    row = source_grid[nr]
                    if 0 <= nc < len(row):
                        points.append(row[nc])
        if points:
            neighbors[key] = points

    return neighbors
