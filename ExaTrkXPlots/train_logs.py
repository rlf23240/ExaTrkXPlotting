#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.train_log', ['history'])
def train_log(ax, data, tag=None, steps_per_epoch=1, label=None):
    history = data['history']
    if tag is None and isinstance(history, list):
        values = history
    else:
        values = history[tag]

    train_epochs = np.arange(0, len(values), 1.0/steps_per_epoch)
    ax.plot(train_epochs, values, label=label)

    if label is not None:
        ax.legend()
