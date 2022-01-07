#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plots about hits (nodes) in ExaTrkX routine.

For plot data requirement, detail list below:
    - hits:
        - required: hit_id, x, y, z or r, phi, z
    - pairs:
        - required: hit_id_1, hit_id_2
    - edges:
        - required: hit_id_1, hit_id_2,
        - optional: score
    - particles:
        - required: particle_id
        - optional: vx, vy, vz, parent_pid
    - truth:
        - required: hit_id, particle_id

For required columns, it use for all plot require this type of dataframe.
For optional columns, it use for special purpose and not required for all plots.
"""

import numpy as np
import pandas as pd

from ExaTrkXPlotting import plot


@plot('exatrkx.hits.2d', ['hits'])
def hit_plot(ax, data, hit_filter=None, label=None, color=None):
    """
    Plot hit 2D positions. Require hits dataframe.
    """
    hits = data['hits']

    if hit_filter is not None:
        hits = hits[hit_filter]

    if all(pd.Series(['x', 'y']).isin(hits.columns)):
        x, y = hits['x'], hits['y']
    elif all(pd.Series(['r', 'phi']).isin(hits.columns)):
        # Cylindrical coord.
        r = hits['r']
        phi = hits['phi']

        # Compute cartesian coord
        x = r * np.cos(phi)
        y = r * np.sin(phi)
    else:
        raise KeyError('No valid coordinate data found.')

    ax.scatter(
        x, y,
        s=1.0,
        label=label,
        color=color
    )

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.axis('equal')

    if label is not None:
        ax.legend()
