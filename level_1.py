def levels(level_num: int) -> list:
    match level_num:
        case 1:
            return [
                [0] * 8,
                [1] * 8,
                [0] * 8,
                [1] * 8,
                [0] * 8,
                [1] * 8
            ]
        case 2:
            return [
                [2, 1, 0, 2, 1, 0, 2, 0, 2, 0, 2, 1, 2],
                [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                [3, 0, 0, 3, 1, 0, 3, 1, 3, 0, 1, 3, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
                [2, 1, 0, 2, 1, 0, 2, 0, 2, 0, 2, 0, 2]
            ]
        case 3:
            return [
                [1] * 4 + [0] * 4,
                [0] * 4 + [2] * 4,
                [3] * 4 + [0] * 4,
                [0] * 4 + [1] * 4,
                [2] * 4 + [0] * 4,
                [0] * 4 + [3] * 4,
                [1] * 4 + [0] * 4,
                [0] * 4 + [2] * 4,
                [3] * 4 + [0] * 4
            ]
        case 5:
            return [
                [0] * 8,
                [0] * 8,
                [2] * 8,
                [0] * 8,
                [0] * 8,
                [0, 0, 0, 0, 1, 0, 0, 0]
            ]
