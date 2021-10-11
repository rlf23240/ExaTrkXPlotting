#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from ExaTrkXPlotting import plotter

try:
    from tensorboard.backend.event_processing import event_accumulator

    @plotter.plot('exatrkx.train_log.tb', ['events'])
    def tb_train_log(ax, data, scalar_tag, steps_per_epoch=1, label=None):
        events = data['events']

        train_loss = pd.DataFrame(events.Scalars(scalar_tag))
        train_epochs = (train_loss['step'] + 1) / steps_per_epoch

        ax.plot(train_epochs, train_loss['value'], label=label)

        if label is not None:
            ax.legend()
except ImportError:
    @plotter.plot('exatrkx.train_log.tb', ['events'])
    def tb_train_log(ax, data, scalar_tag, steps_per_epoch=1, label=None):
        raise RuntimeError(
            'Tensorboard not install. '
            'Please install TensorFlow or Tensorboard only to use this plot.'
        )
