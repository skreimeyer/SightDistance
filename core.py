import math
from enum import Enum

# Globals
REACTION_TIME = 2.5  # seconds
DECELERATION_RATE = 11.2  # ft/s^2

class Maneuver(Enum):
    A = 3.0
    B = 9.1
    C = 10.2
    D = 12.1
    E = 14.0

    @classmethod
    def list_maneuvers(cls):
        return [m for m in cls]

    @classmethod
    def describe(cls):
        summary = """A: Stop on a road in a rural area
        B: Stop on a road in an urban area
        C: Speed/path/direction change in a rural area
        D: Speed/path/direction change in an suburban area
        E: Speed/path/direction change in an urban area"""
# Functions
# convert miles per hour to feet per second
def mph_to_fps(mph):
    return mph * 5280 / 3600


# calculate the distance required to stop at a given speed (in miles per hour)
def braking_distance(speed, G=0.0):
    if G != 0.0:
        return speed**2 / (30*(DECELERATION_RATE/32.2+G))
    return 1.075 * speed**2 / DECELERATION_RATE


# round a number up to the nearest 5
def round_to_5(num):
    return math.ceil(num / 5) * 5


# calculate stopping sight distance in feet by AASHTO method
def stopping_sight_distance(mph, G=0.0):
    brake_reaction_distance = mph_to_fps(mph) * REACTION_TIME
    brake_distance = braking_distance(mph,G)
    return round_to_5(brake_reaction_distance + brake_distance)


# calculate sagitta of a circle given a radius and chord length. Assumes chord is always in minor arc.
def sagitta(r, c):
    inner_term = r**2 - c**2/4
    if inner_term < 0:
        return 0
    result = r - math.sqrt(inner_term)
    return result

def hso(r, mph=70, lanes=1, lane_width=12.0, G=0.0, median_offset=0.0):
    outside_travel_radius = r - median_offset - lane_width * (lanes-0.5)
    ssd = stopping_sight_distance(mph,G)
    sag = sagitta(outside_travel_radius, ssd)
    return sag

# calculate minimum clear horizontal offset from the edge of traveled way.
def clear_offset(r, mph=70, lanes=1, lane_width=12.0, G=0.0, median_offset=0.0):
    outside_travel_radius = r - median_offset - lane_width * (lanes-0.5)
    ssd = stopping_sight_distance(mph,G)
    sag = sagitta(outside_travel_radius, ssd)
    return max(sag - lane_width*0.5, 0)

def clear_inside_shoulder(base_radius, mph=70, G=0.0, min_offset=1.0, is_clear=True):
    if not is_clear:
        base_radius = base_radius + min_offset
        min_offset = 0
    for offset in range(math.ceil(min_offset), 100, 1):
        hso = clear_offset(base_radius+offset, mph=mph, lanes=0, G=G)
        if hso < offset:
            return max(offset-min_offset,0)
    return 0

# calculate decision sight distance for one of five avoidance maneuvers labeled "A", "B", "C", "D", or "E"
def decision_sight_distance(mph: int, maneuver: Maneuver, G=0.0) -> float:
    if maneuver == Maneuver.A or maneuver == Maneuver.B:
        dsd = 1.47*mph*maneuver.value+braking_distance(mph, G)
    else:
        dsd = 1.47*mph*maneuver.value * adjust_maneuver(maneuver, mph)
    return round_to_5(dsd)

# AASHTO tables use a range of reaction times which are distributed nearly as a step function.
# This is approximately the minimum maneuver range, then the maximum time for 60 and 65mph speeds
# then drop to half the difference for higher speeds
def adjust_maneuver(maneuver: Maneuver, speed: float) -> float:
    def factor(speed,max_adjust):
        if speed < 60:
            return 1.0
        if speed < 65:
            return 1.0+(max_adjust)
        return 1.0+(max_adjust)/2

    if maneuver == Maneuver.C:
        return factor(speed,0.1)
    if maneuver == Maneuver.D:
        return factor(speed,0.05)
    if maneuver == Maneuver.E:
        return factor(speed,0.03)


def feet_to_station(ft):
    return ft / 100
