#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from ExaTrkXPlotting import plotter, PlotConfig


@plotter.plot('example.1', ['x1', 'y1'])
def test_plot_1(ax, data):
    ax.plot(data['x1'], data['y1'])


@plotter.plot('example.2', ['x2', 'y2'])
def test_plot_2(ax, data):
    ax.plot(data['x2'], data['y2'])


if __name__ == '__main__':
    # Assign data for each plot.
    fig, axes = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
    plotter.plot_figure(fig, {
        axes[0][0]: PlotConfig(
            plot='example.1',
            data={
                'x1': [1, 2, 3],
                'y1': [1, 2, 3]
            },
            args={}
        ),
        axes[0][1]: PlotConfig(
            plot='example.1',
            data={
                'x1': [1, 2, 3],
                'y1': [3, 2, 3]
            },
            args={}
        ),
        axes[1][0]: PlotConfig(
            plot='example.1',
            data={
                'x1': [1, 2, 3],
                'y1': [3, 2, 3]
            },
            args={}
        ),
        axes[1][1]: PlotConfig(
            plot='example.1',
            data={
                'x1': [1, 2, 3],
                'y1': [1, 2, 1]
            },
            args={}
        )
    }, save='output/full_config.png')

    # Assign same data to all plot.
    fig, axes = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
    plotter.plot_figure(fig, {
        axes[0][0]: PlotConfig('example.1'),
        axes[0][1]: PlotConfig('example.1'),
        axes[1][0]: PlotConfig('example.2'),
        axes[1][1]: PlotConfig('example.2'),
    }, data={
        'x1': [1, 2, 3],
        'y1': [1, 2, 3],
        'x2': [1, 2, 3],
        'y2': [3, 2, 1]
    }, save='output/assign_same_data.png')

    # Use config file and overlap multiple plot on same axis.
    fig, axes = plt.subplots(2, 2, figsize=(8, 8), tight_layout=True)
    plotter.plot_figure(
        fig, {
            axes[0][0]: PlotConfig(config='config.1'),
            axes[0][1]: PlotConfig(config='config.2'),
            axes[1][0]: PlotConfig(
                config='config.1',
                data={
                    'x1': [1, 2, 3],
                    'y1': [3, 2, 1]
                }
            ),
            axes[1][1]: [
                PlotConfig(config='config.1'),
                PlotConfig(config='config.2')
            ]
        },
        config='configs/example.yaml',
        data={
            'x1': [1, 2, 3],
            'y1': [1, 2, 3],
            'x2': [1, 2, 3],
            'y2': [3, 2, 1]
        },
        save='output/config_overlap.png'
    )
