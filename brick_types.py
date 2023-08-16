types = {
    1: {
        "type": "classic",
        "health": 2,
        "images": ['img/bricks/brick1.png',
                   'img/bricks/brick2.png'
                   ]
    },
    2: {
        "type": "bonus_pb",
        "health": 1,
        "images": ['img/bricks/brickPB.png']
    },
    3: {
        "type": "bonus_ps",
        "health": 1,
        "images": ['img/bricks/brickPS.png']
    }
}


def brick_type(type_brick):
    return types[type_brick]