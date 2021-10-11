#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plots about hit pairs (edges) in ExaTrkX routine.

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

from typing import Any

import pandas as pd
from matplotlib import collections as mc

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.hit_pairs.2d', ['hits', 'pairs'])
def hit_pair_plot(ax, data, line_width=0.1, label=None, color=None):
    """
    Plot hit pair 2D connections. Require hits dataframe and pairs dataframe.
    """
    hits = data['hits']
    pairs = data['pairs']

    pairs = pd.merge(
        pairs, hits,
        left_on='hit_id_1',
        right_on='hit_id'
    )
    pairs = pairs.merge(
        pairs, hits,
        left_on='hit_id_2',
        right_on='hit_id',
        suffixes=('_1', '_2')
    )

    positions = pairs[['x_1', 'y_1', 'x_2', 'y_2']].to_numpy()
    position_pairs = [((x1, y1), (x2, y2)) for x1, y1, x2, y2 in positions]
    line_collection = mc.LineCollection(
        position_pairs,
        linewidths=line_width,
        color=color,
        label=label
    )
    ax.add_collection(line_collection)

    if label is not None:
        ax.legend()


@plotter.plot('exatrkx.hit_pairs.hist', ['edges'])
def edge_hist(
    ax,
    data,
    feature: str,
    bins=None,
    edge_filter=None,
    log_scale: bool = False,
    normalize: bool = False,
    label: str = None,
    color: Any = None
):
    """
    Plot edge histogram. Require edges dataframe.
    Columns use by feature and edge_filter should also be exist in edges dataframe.
    """
    edges = data['edges']
    if edge_filter is not None:
        edges = edges[edge_filter]

    ax.set_xlabel(feature)
    ax.hist(
        edges[feature],
        histtype='step',
        lw=2,
        bins=bins,
        log=log_scale,
        density=normalize,
        label=label,
        color=color
    )

    if label is not None:
        ax.legend()
