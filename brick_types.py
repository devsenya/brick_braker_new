types = {
    "classic": {
        "type": "classic",
        "health": 2,
        "images": ['img/bricks/brick1.png',
                   'img/bricks/brick2.png'
                   ]
    },
    "bonus_pb": {
        "type": "bonus_pb",
        "health": 1,
        "images": ['img/bricks/brickPB.png']
    }
}


def brick_type(type_brick):
    return types[type_brick]

print(brick_type("bonus_pb"))