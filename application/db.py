import os
import json


class Database(object):
    proxy = None

    def __init__(self):
        if not os.path.exists("out/db.json"):
            with open("out/db.json", "w") as dbfile:
                json.dump({
                    "gray": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "basic": {
                                "pid": 31007,
                                "vals": []
                            },
                            "lampholder": {
                                "pid": 38217,
                                "vals": []
                            },
                            "static1x1": {
                                "pid": 36304,
                                "vals": []
                            }
                        }
                    },
                    "red": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "30x1/3": {
                                "pid": 35049,
                                "vals": []
                            },
                            "15x1/3": {
                                "pid": 37237,
                                "vals": []
                            },
                            "60deg": {
                                "pid": 31010,
                                "vals": []
                            },
                            "bearing": {
                                "pid": 32064,
                                "vals": []
                            },
                            "reedclip": {
                                "pid": 35969,
                                "vals": []
                            },
                            "staticconnector": {
                                "pid": 36973,
                                "vals": []
                            },
                            "minigear": {
                                "pid": 31020,
                                "vals": []
                            },
                            "wheel": {
                                "pid": 36581,
                                "vals": []
                            }
                        }
                    },
                    "green": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "cap": {
                                "pid": 35084,
                                "vals": []
                            }
                        }
                    },
                    "blue": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "cap": {
                                "pid": 35077,
                                "vals": []
                            }
                        }
                    },
                    "black": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "lampholder": {
                                "pid": 38216,
                                "vals": []
                            },
                            "basic": {
                                "pid": 32881,
                                "vals": []
                            },
                            "wheel": {
                                "pid": 36574,
                                "vals": []
                            },
                            "miniwheel": {
                                "pid": 36573,
                                "vals": []
                            },
                            "staticconector": {
                                "pid": 32850,
                                "vals": []
                            }
                        }
                    },
                    "yellow": {
                        "bounds": {
                            "upper": [0, 0, 0],
                            "lower": [255, 255, 255],
                        },
                        "parts": {
                            "cap": {
                                "pid": 35085,
                                "vals": []
                            },
                            "basic": {
                                "pid": 36529,
                                "vals": []
                            },
                            "static1x1": {
                                "pid": 36298,
                                "vals": []
                            }
                        }
                    }
                }, dbfile)

        with open("out/db.json", "r") as dbfile:
            self.proxy = json.load(dbfile)

    def save(self):
        with open("out/db.json", "w") as dbfile:
            json.dump(self.proxy, dbfile)

db = Database()
