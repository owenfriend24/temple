# output is not super well-structured in the txt files on tacc but it is consistent
#   later can go back and figure out a more logical way to generate these
#   but for now hard-coded will work fine
def pull_across_symm_indices(triad):
    across_indices = [[9, 12, 15, 18, 21, 24, 27, 30, 33, 45, 48, 51, 54, 57,
                       60, 63, 66, 69, 81, 84, 87, 90, 93, 96, 99, 102, 105],
                      [0, 3, 6, 19, 22, 25, 28, 31, 34, 36, 39, 42, 55, 58, 61,
                       64, 67, 70, 72, 75, 78, 91, 94, 97, 100, 103, 106],
                      [1, 4, 7, 10, 13, 16, 29, 32, 35, 37, 40, 43, 46, 49, 52,
                       65, 68, 71, 73, 76, 79, 82, 85, 88, 101, 104, 107],
                      [2, 5, 8, 11, 14, 17, 20, 23, 26, 38, 41, 44, 47, 50, 53,
                       56, 59, 62, 74, 77, 80, 83, 86, 89, 92, 95, 98]]
    return across_indices[(triad-1)]

def pull_within_symm_indices(triad):
    start = (triad - 1) * 3
    return [start + i + j * 12 for j in range(3) for i in range(3)]
    # within_indices = [[0, 1, 2, 12, 13, 14, 24, 25, 26],
    #                   [3, 4, 5, 15, 16, 17, 27, 28, 29],
    #                   [6, 7, 8, 18, 19, 20, 30, 31, 32],
    #                   [9, 10, 11, 21, 22, 23, 33, 34, 35]]

def pull_within_symm_indices_droprun(triad):
    start = (triad - 1) * 2  # Each triad starts at (triad - 1) * 2
    indices = [(start + i, start + i + 8, start + i + 16) for i in range(2)]
    return [num for pair in indices for num in pair]


def pull_across_symm_indices_droprun(triad):
    across_indices = [[6, 9, 12, 15, 18, 21, 30, 33, 36, 39, 42, 45, 54, 57, 60, 63, 66, 69],
                      [0, 3, 13, 16, 19, 22, 24, 27, 37, 40, 43, 46, 48, 51, 61, 64, 67, 70],
                      [1, 4, 7, 10, 20, 23, 25, 28, 31, 34, 44, 47, 49, 52, 55, 58, 68, 71],
                      [2, 5, 8, 11, 14, 17, 26, 29, 32, 35, 38, 41, 50, 53, 56, 59, 62, 65]]

# takes in an int 1, 2, 3, or 4
def pull_within_prepost_indices(triad):
    indices = []
    for comp_run in range(4):
        indices.append((triad - 1) * 4 + comp_run)

    for comp_run in range(2):
        indices.append(16 + (triad - 1) * 2 + comp_run)
    return indices


# takes in an int 1, 2, 3, or 4
def pull_across_prepost_indices(triad):
    indices = []
    start_1 = (triad - 1) * 12
    indices.extend(range(start_1, start_1 + 12))
    start_2 = 48 + (triad - 1) * 6
    indices.extend(range(start_2, start_2 + 6))
    return indices

# takes in an int 1, 2, 3, or 4
def pull_within_prepost_indices_droprun(triad):
    start = (triad*2)-2
    indices = [start, start + 1]
    return indices


def pull_across_prepost_indices_droprun(triad):
    start = (triad-1) * 6
    indices = list(range(start, start + 6))
    return indices
