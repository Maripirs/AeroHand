
ASL_ALPHABET = {
    "A": {
        "pose": [10, 55, 23, 80, 80, 80, 90],
        "status": "supported",
        "notes": "Closed fist approximation. Fingers close first, then thumb moves across.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 80,
                    4: 80,
                    5: 80,
                    6: 90,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 10,
                    1: 55,
                    2: 23,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 10,
                    1: 55,
                    2: 23,
                },
                "duration": 0.5,
            },
        ],
    },

    "B": {
        "pose": [20, 100, 70, 0, 0, 0, 0],
        "status": "supported",
        "notes": "Flat hand with thumb folded across palm.",
        "sequence": None,
    },

    "C": {
        "pose": [100, 20, 30, 45, 45, 45, 45],
        "status": "supported",
        "notes": "Curved C handshape approximation.",
        "sequence": None,
    },

    "D": {
        "pose": [100, 25, 30, 0, 55, 55, 55],
        "status": "supported",
        "notes": "Index extended, other fingers curled.",
        "sequenMaripi/alphabet.pyce": None,
    },

    "E": {
        "pose": [100, 25, 30, 55, 55, 55, 55],
        "status": "questionable",
        "notes": "Compact E shape. Fingers move first, then thumb settles into position.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 55,
                    4: 55,
                    5: 55,
                    6: 55,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 100,
                    1: 25,
                    2: 30,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 100,
                    1: 25,
                    2: 30,
                },
                "duration": 0.5,
            },
        ],
    },

    "F": {
        "pose": [80, 25, 35, 45, 0, 0, 0],
        "status": "supported",
        "notes": "Approximate index-thumb contact with other fingers extended.",
        "sequence": [
            {
                "set": {
                    4: 0,
                    5: 0,
                    6: 0,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 25,
                    2: 35,
                    3: 45,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 25,
                    2: 35,
                    3: 45,
                },
                "duration": 0.5,
            },
        ],
    },

    "G": {
        "pose": [40, 80, 30, 0, 90, 90, 90],
        "status": "needs_baxter",
        "notes": "Handshape can be approximated, but correct ASL G requires arm/wrist orientation.",
        "sequence": None,
    },

    "H": {
        "pose": [80, 100, 40, 0, 0, 90, 90],
        "status": "needs_baxter",
        "notes": "Requires arm/wrist orientation for proper ASL presentation.",
        "sequence": None,
    },

    "I": {
        "pose": [80, 40, 40, 90, 90, 90, 0],
        "status": "supported",
        "notes": "Pinky extended. Thumb gets out of the way, fingers close, then thumb comes over/across.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 90,
                    4: 90,
                    5: 90,
                    6: 0,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 40,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 40,
                    2: 40,
                },
                "duration": 0.5,
            },
        ],
    },

    "J": {
        "pose": [80, 40, 40, 90, 90, 90, 0],
        "status": "needs_baxter",
        "notes": "Uses the I handshape, but ASL J requires drawing motion.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 90,
                    4: 90,
                    5: 90,
                    6: 0,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 40,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 80,
                    1: 40,
                    2: 40,
                },
                "duration": 0.5,
            },
        ],
    },

    "K": {
        "pose": [50, 80, 40, 0, 20, 90, 90],
        "status": "questionable",
        "notes": "Thumb placement between index and middle is difficult.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 20,
                    5: 90,
                    6: 90,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 50,
                    1: 80,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 50,
                    1: 80,
                    2: 40,
                },
                "duration": 0.5,
            },
        ],
    },

    "L": {
        "pose": [0, 0, 0, 0, 90, 90, 90],
        "status": "supported",
        "notes": "Thumb and index extended, other fingers curled.",
        "sequence": None,
    },

    "M": {
        "pose": [100, 100, 40, 60, 60, 60, 60],
        "status": "questionable",
        "notes": "Thumb moves first, then fingers close over it.",
        "sequence": [
            {
                "set": {
                    0: 100,
                    1: 100,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 60,
                    4: 60,
                    5: 60,
                    6: 60,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 60,
                    4: 60,
                    5: 60,
                    6: 60,
                },
                "duration": 0.5,
            },
        ],
    },

    "N": {
        "pose": [70, 100, 40, 60, 60, 60, 60],
        "status": "questionable",
        "notes": "Thumb moves first, then fingers close.",
        "sequence": [
            {
                "set": {
                    0: 70,
                    1: 100,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 60,
                    4: 60,
                    5: 60,
                    6: 60,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 60,
                    4: 60,
                    5: 60,
                    6: 60,
                },
                "duration": 0.5,
            },
        ],
    },

    "O": {
        "pose": [100, 30, 30, 50, 50, 50, 50],
        "status": "supported",
        "notes": "Rounded O approximation.",
        "sequence": None,
    },

    "P": {
        "pose": [50, 80, 40, 0, 20, 90, 90],
        "status": "needs_baxter",
        "notes": "Similar to K handshape, but ASL P requires downward orientation.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 20,
                    5: 90,
                    6: 90,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 50,
                    1: 80,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 50,
                    1: 80,
                    2: 40,
                },
                "duration": 0.5,
            },
        ],
    },

    "Q": {
        "pose": [40, 90, 15, 20, 90, 90, 90],
        "status": "needs_baxter",
        "notes": "Requires downward orientation.",
        "sequence": None,
    },

    "R": {
        "pose": [70, 100, 50, 0, 0, 90, 90],
        "status": "not_possible",
        "notes": "True ASL R requires crossed fingers, which this hand cannot perform.",
        "sequence": None,
    },

    "S": {
    "pose": [90, 100, 30, 80, 80, 80, 90],
    "status": "supported",
    "notes": "Thumb moves to neutral, fingers close, then thumb comes over/across.",
    "sequence": [
        {
            "set": {
                0: 40,
                1: 40,
                2: 30,
            },
            "duration": 0.5,
        },
        {
            "set": {
                3: 80,
                4: 80,
                5: 80,
                6: 90,
            },
            "duration": 0.5,
        },
        {
            "set": {
                0: 90,
                1: 100,
                2: 30,
            },
            "duration": 0.5,
        },
        {
            "set": {
                0: 90,
                1: 100,
                2: 30,
            },
            "duration": 0.5,
        },
    ],
},

    "T": {
        "pose": [70, 85, 40, 50, 100, 100, 100],
        "status": "not_possible",
        "notes": "Thumb-between-fingers shape is mechanically difficult; sequence reduces collision risk.",
        "sequence": [
            {
                "set": {
                    0: 0,
                    1: 0,
                    2: 0,
                    4: 100,
                    5: 100,
                    6: 100,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    0: 70,
                    1: 85,
                    2: 40,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 50,
                },
                "duration": 0.5,
            },
            {
                "set": {
                    3: 50,
                },
                "duration": 0.5,
            },
        ],
    },

    "U": {
        "pose": [100, 100, 30, 0, 0, 90, 90],
        "status": "supported",
        "notes": "Index and middle extended.",
        "sequence": None,
    },

    "V": {
        "pose": [100, 100, 30, 0, 0, 90, 90],
        "status": "not_possible",
        "notes": "Uses same pose as U because this hand cannot separate/spread the index and middle fingers.",
        "sequence": None,
    },

    "W": {
        "pose": [100, 100, 30, 0, 90, 90, 90],
        "status": "questionable",
        "notes": "Approximation is limited by finger independence and spacing.",
        "sequence": None,
    },

    "X": {
        "pose": [100, 100, 30, 30, 90, 90, 90],
        "status": "questionable",
        "notes": "Hooked index approximation.",
        "sequence": None,
    },

    "Y": {
        "pose": [0, 90, 0, 90, 90, 90, 0],
        "status": "questionable",
        "notes": "Thumb and pinky extended; exact shape may be limited.",
        "sequence": None,
    },

    "Z": {
        "pose": [100, 100, 30, 0, 90, 90, 90],
        "status": "needs_baxter",
        "notes": "Requires drawing motion for Z.",
        "sequence": None,
    },
}