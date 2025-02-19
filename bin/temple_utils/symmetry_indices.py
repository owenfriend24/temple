# output is not super well-structured in the txt files but it is consistent
#   later can go back and figure out a more logical way to generate these
#   but for now hard-coded will work fine
def pull_across_indices(triad):
    across_indices = [[9, 12, 15, 18, 21, 24, 27, 30, 33, 45, 48, 51, 54, 57,
                       60, 63, 66, 69, 81, 84, 87, 90, 93, 96, 99, 102, 105],
                      [0, 3, 6, 19, 22, 25, 28, 31, 34, 36, 39, 42, 55, 58, 61,
                       64, 67, 70, 72, 75, 78, 91, 94, 97, 100, 103, 106],
                      [1, 4, 7, 10, 13, 16, 29, 32, 35, 37, 40, 43, 46, 49, 52,
                       65, 68, 71, 73, 76, 79, 82, 85, 88, 101, 104, 107],
                      [2, 5, 8, 11, 14, 17, 20, 23, 26, 38, 41, 44, 47, 50, 53,
                       56, 59, 62, 74, 77, 80, 83, 86, 89, 92, 95, 98]]
    return across_indices[(triad-1)]

def pull_within_indices(triad):
    within_indices = [[0, 1, 2, 12, 13, 14, 24, 25, 26],
                      [3, 4, 5, 15, 16, 17, 27, 28, 29],
                      [6, 7, 8, 18, 19, 20, 30, 31, 32],
                      [9, 10, 11, 21, 22, 23, 33, 34, 35]]
    return within_indices[(triad-1)]