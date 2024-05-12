# Horizontal Sight Distance

Motor vehicle operators must be able to see ahead to safely react to
highway conditions that require stopping or changing speed or direction.
This application is meant to facilitate the common calculations of
stopping sight distance, clear offsets, and decision sight distance.

## Stopping Sight Distance

*Stopping sight distance is the sum of two distances: (1) the distance traversed by the vehicle
from the instant the driver sights an object necessitating a stop to the instant the brakes are ap-
plied, and (2) the distance needed to stop the vehicle from the instant brake application begins.
These are referred to as brake reaction distance and braking distance, respectively.*

-- *A Policy on Geometric Design of Highways and Streets 7th Ed. (AASHTO, 2018)*

Stopping sight distance is calculated as follows:

$$
SSD = 1.47Vt + 1.075\frac{V^2}{a}
$$

where:
- *SSD* = stopping sight distance
- *V* = velocity (mph)
- *t* = reaction time (2.5s)
- *a* = deceleration rate (11.2ft/s<sup>2</sup>)


