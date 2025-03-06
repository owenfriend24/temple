# output is not super well-structured in the txt files on tacc but it is consistent
#   later can go back and figure out a more logical way to generate these
#   but for now hard-coded will work fine


### SYMMETRY ###

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
    return across_indices[(triad-1)]





### PREPOST ###

# takes in an int 1, 2, 3, or 4; works for any AB, AC, or BC pairing
def pull_within_prepost_indices(triad):
    indices = []
    for comp_run in range(4):
        indices.append((triad - 1) * 4 + comp_run)

    for comp_run in range(2):
        indices.append(16 + (triad - 1) * 2 + comp_run)
    return indices

# for full triplet at once, this can't be the best way to do this ...
def pull_within_ABC_prepost_indices(triad):
    indices = [[0, 4, 8, 12, 13, 20, 21, 28, 29, 144, 148, 152, 156, 157, 164,
                165, 172, 173, 288, 292, 296, 300, 301, 308, 309, 316, 317],
               [37, 41, 45, 50, 51, 58, 59, 66, 67, 181, 185, 189, 194, 195, 202,
                203, 210, 211, 325, 329, 333, 338, 339, 346, 347, 354, 355],
               [74, 78, 82, 88, 89, 96, 97, 104, 105, 218, 222, 226, 232, 233,
               240, 241, 248, 249, 362, 366, 370, 376, 377, 384, 385, 392, 393],
                [111, 115, 119, 126, 127, 134, 135, 142, 143, 255, 259, 263, 270,
                  271, 278, 279, 286, 287, 399, 403, 407, 414, 415, 422, 423, 430, 431]]
    return indices[triad-1]

def pull_within_ABC_prepost_indices_droprun(triad):
    indices = [[0, 1, 8, 9, 16, 17],
               [26, 27, 34, 35, 42, 43],
               [52, 53, 60, 61, 68, 69],
                [78, 79, 86, 87, 94, 95]]
    return indices[triad-1]

# is this supposed to be symmetry?
def pull_across_ABC_prepost_indices(triad):
    indices = [[1, 2, 3, 5, 6, 7, 9, 10, 11, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 34, 35, 145,
                146, 147, 149, 150, 151, 153, 154, 155, 158, 159, 160, 161, 162, 163, 166, 167, 168, 169, 170, 171, 174,
                175, 176, 177, 178, 179, 289, 290, 291, 293, 294, 295, 297, 298, 299, 302, 303, 304, 305, 306, 307, 310,
                311, 312, 313, 314, 315, 318, 319, 320, 321, 322, 323],
               [36, 38, 39, 40, 42, 43, 44, 46, 47, 48, 49, 52, 53, 54, 55, 56, 57, 60, 61, 62, 63, 64, 65, 68, 69, 70,
                71, 180, 182, 183, 184, 186, 187, 188, 190, 191, 192, 193, 196, 197, 198, 199, 200, 201, 204, 205, 206,
                207, 208, 209, 212, 213, 214, 215, 324, 326, 327, 328, 330, 331, 332, 334, 335, 336, 337, 340, 341, 342,
                343, 344, 345, 348, 349, 350, 351, 352, 353, 356, 357, 358, 359],
               [72, 73, 75, 76, 77, 79, 80, 81, 83, 84, 85, 86, 87, 90, 91, 92, 93, 94, 95, 98, 99, 100, 101, 102, 103,
                106, 107, 216, 217, 219, 220, 221, 223, 224, 225, 227, 228, 229, 230, 231, 234, 235, 236, 237, 238, 239,
                242, 243, 244, 245, 246, 247, 250, 251, 360, 361, 363, 364, 365, 367, 368, 369, 371, 372, 373, 374, 375,
                378, 379, 380, 381, 382, 383, 386, 387, 388, 389, 390, 391, 394, 395],
                [108, 109, 110, 112, 113, 114, 116, 117, 118, 120, 121, 122, 123, 124, 125, 128, 129, 130, 131, 132, 133,
                 136, 137, 138, 139, 140, 141, 252, 253, 254, 256, 257, 258, 260, 261, 262, 264, 265, 266, 267, 268, 269,
                 272, 273, 274, 275, 276, 277, 280, 281, 282, 283, 284, 285, 396, 397, 398, 400, 401, 402, 404, 405, 406,
                 408, 409, 410, 411, 412, 413, 416, 417, 418, 419, 420, 421, 424, 425, 426, 427, 428, 429]]
    return indices[triad-1]

def pull_across_ABC_prepost_indices_droprun(triad):
    indices = [[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23],
               [24, 25, 28, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47],
               [48, 49, 50, 51, 54, 55, 56, 57, 58, 59, 62, 63, 64, 65, 66, 67, 70, 71],
                [72, 73, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 88, 89, 90, 91, 92, 93]]
    return indices[triad-1]

# takes in an int 1, 2, 3, or 4
def pull_across_prepost_indices(triad):
    indices = []
    start_1 = (triad - 1) * 12
    indices.extend(range(start_1, start_1 + 12))
    start_2 = 48 + (triad - 1) * 6
    indices.extend(range(start_2, start_2 + 6))
    return indices

print(pull_across_prepost_indices(4))

# takes in an int 1, 2, 3, or 4
def pull_within_prepost_indices_droprun(triad):
    start = (triad*2)-2
    indices = [start, start + 1]
    return indices

def pull_across_prepost_indices_droprun(triad):
    start = (triad-1) * 6
    indices = list(range(start, start + 6))
    return indices
