#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plots about particles in ExaTrkX routine.

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

import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.particles.production_vertex', ['pairs', 'truth', 'particles'])
def production_vertices(ax, data):
    pairs = data['pairs']
    truth = data['truth']
    particles = data['particles']

    hits_with_particles = pd.merge(
        truth, particles,
        how='inner'
    )

    pairs_with_pid = pd.merge(
        pairs,
        hits_with_particles,
        left_on='hit_id_1',
        right_on='hit_id',
        how="inner"
    )

    # Group by vertex.
    pairs_group_by_vertices = pairs_with_pid.groupby(['vx', 'vy', 'vz'])

    # Create color map.
    colors = plt.cm.get_cmap('gunplot', len(pairs_group_by_vertices) + 1)

    for idx, (vertex, pairs) in enumerate(pairs_group_by_vertices):
        vx, vy, vz = vertex
        vr = math.sqrt(vx ** 2 + vy ** 2)

        # Get color.
        color = colors(idx)

        ax.scatter(
            vz, vr,
            marker='+',
            color=color,
            label=f'({vz}, {vr})'
        )


@plotter.plot('exatrkx.particles.types', ['pairs', 'truth', 'particles'])
def particle_types(ax, data):
    pairs = data['pairs']
    truth = data['truth']
    particles = data['particles']

    hits_with_particles = pd.merge(
        truth, particles,
        how='inner'
    )

    pairs_with_pid = pd.merge(
        pairs,
        hits_with_particles,
        left_on='hit_id_1',
        right_on='hit_id',
        how="inner"
    )

    # Group by vertex.
    pairs_group_by_vertices = pairs_with_pid.groupby(['vx', 'vy', 'vz'])

    for idx, (vertex, pairs) in enumerate(pairs_group_by_vertices):
        for particle_id, tracks in pairs.groupby('particle_id'):
            # particle_type = particle_types[int(tracks['particle_type'].iloc[0])]
            particle_type = int(tracks['particle_type'].iloc[0])

            if 'r_2' not in tracks.columns:
                tracks['r_2'] = np.sqrt(tracks['x_2']**2 + tracks['y_2']**2)

            r2, z2 = tracks.loc[
                tracks['r_2'].idxmax()
            ][['r_2', 'z_2']]
            ax.annotate(particle_type, (z2, r2))
