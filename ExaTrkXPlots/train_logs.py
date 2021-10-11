#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib.ticker import MaxNLocator

from ExaTrkXPlotting import plotter


@plotter.plot('exatrkx.train_log', ['history'])
def train_log(ax, data, tag=None, y_label=None, steps_per_epoch=1, label=None):
    history = data['history']
    if tag is None:
        values = history
    else:
        values = history[tag]

    train_epochs = np.arange(0, len(values), 1.0/steps_per_epoch)
    ax.plot(train_epochs, values, label=label)

    ax.set_xlabel('Epochs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    if y_label is not None:
        ax.set_ylabel(y_label)

    if label is not None:
        ax.legend()
