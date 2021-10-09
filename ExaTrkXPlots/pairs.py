#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

import pandas as pd
from matplotlib import collections as mc

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.hit_pairs.2d', ['hits', 'pairs'])
def hit_pair_plot(ax, data, line_width=0.1, label=None, color=None):
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
