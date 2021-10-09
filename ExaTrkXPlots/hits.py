#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.hits.2d', ['hits'])
def hit_plot(ax, data, hit_filter=None, label=None, color=None):
    hits = data['hits']

    if hit_filter is not None:
        hits = hits[hit_filter]

    ax.scatter(
        hits['x'], hits['y'],
        s=1.0,
        label=label,
        color=color
    )

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.axis('equal')

    if label is not None:
        ax.legend()
