## Horizontal Sight Offset

*On a tangent roadway, the obstruction that limits the driver’s sight distance is the road surface at
some point on a crest vertical curve. On horizontal curves, the obstruction that limits the driver’s
sight distance may be the road surface at some point on a crest vertical curve or it may be some
physical feature outside of the traveled way, such as a longitudinal barrier, a bridge-approach
fill slope, a tree, foliage, or the backslope of a cut section. Accordingly, all highway construction
plans should be checked in both the vertical and horizontal plane for sight distance obstructions.*

-- *A Policy on Geometric Design of Highways and Streets 7th Ed. (AASHTO, 2018)*

Horizontal sight offset is a common roadway design calculation that measures
the distance from the traveled way that should be free of obstruction
for a curve of a given radius and design speed.

This application computes horizontal sight offsets as the saggita of a
circular arc as measured from the middle of the lane.

$$
s = r - \sqrt{\frac{r^2}{\frac{c^2}{4}}}
$$

where:
- *s = saggita (ft) (distance from the chord to the arc)*
- *r = radius (ft)*
- *c = chord-length (ft) (stopping sight distance)*

$$
r_{effective} = r - m - l_{w}(n-\frac{1}{2})
$$

$$
HSO = s - \frac{1}{2}w_{l}
$$

where:
- *r<sub>effective</sub> = radius at travel path (ft)*
- *m = median width (ft)*
- *l<sub>w</sub> = lane width (ft)*
- *n = number of lanes*
- *s = saggita (ft) (of effective radius and SSD)*
- *HSO = Horizontal Sight Offset (ft)*
