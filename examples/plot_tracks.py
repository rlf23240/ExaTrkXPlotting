#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Plotter.
from ExaTrkXPlotting import plotter, PlotConfig

# Include track plots.
import ExaTrkXPlots.tracks

if __name__ == '__main__':
    fig, ax = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)

    with pd.HDFStore('data/tracks/tracks.npz', 'r') as fp:
        df = fp['data']

    generated = df
    reconstructable = df[df.is_trackable]
    matched = df[df.is_trackable & df.is_matched]

    plotter.plot_figure(
        fig, {
            ax[0, 0]: PlotConfig(
                plot='exatrkx.tracks.distribution',
                args={
                    'x_variable': 'pt',
                    'x_label': '$p_T$ [GeV]',
                    'bins': np.arange(0, 10.5, 0.5)
                }
            ),
            ax[0, 1]: PlotConfig(
                plot='exatrkx.tracks.efficiency',
                args={
                    'x_variable': 'pt',
                    'x_label': '$p_T$ [GeV]',
                    'bins': np.arange(0, 10.5, 0.5)
                }
            ),
            ax[1, 0]: PlotConfig(
                plot='exatrkx.tracks.distribution',
                args={
                    'x_variable': 'eta',
                    'x_label': r'$\eta$',
                    'bins': np.arange(-4.4, 4.4, 0.4)
                }
            ),
            ax[1, 1]: PlotConfig(
                plot='exatrkx.tracks.efficiency',
                args={
                    'x_variable': 'eta',
                    'x_label': r'$\eta$',
                    'bins': np.arange(-4.4, 4.4, 0.4)
                }
            )
        },
        data={
            'generated': generated,
            'reconstructable': reconstructable,
            'matched': matched
        }
    )
