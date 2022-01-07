#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict, Any, AnyStr
from os import PathLike
from pathlib import Path
from time import time

import yaml

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .plot_config import PlotConfig
from .plot_manager import plot_manager


class Plotter:
    def __init__(
        self,
        fig: Figure,
        axes: Union[np.ndarray, Axes, Dict[Axes, PlotConfig]],
        data: Any = None,
        config: Any = None,
        # Figure level settings.
        # TODO: rcParam support?
        font: dict = None,
        font_size: int = None
    ):
        """
        Plotter of a figure.

        :param fig:
            matplotlib Figure object.
        :param axes:
            Configurations define how to plot each axes.
        :param config:
            Single or list of external configuration file path or config dict.
        :param data:
            Data pass to all plotting function if no data assign in configuration.
        :param font:
            Dictionary with font setting.
        :param font_size:
            Font size. If set it will overwrite setting in font parameter.
        """
        self.fig = fig
        if isinstance(axes, Axes):
            self.plots = {axes: None}
        elif isinstance(axes, np.ndarray):
            self.plots = dict.fromkeys(axes.flatten())
        elif isinstance(axes, dict):
            self.plots = axes

        self.config = config
        self.data = data
        self.font = font
        self.font_size = font_size

    def plot(
        self, save: Union[PathLike, AnyStr] = None
    ):
        """
        Plot the figure.

        :param save:
            Figure save location. None if you want to show plot instead of save it.
        """
        if self.font is not None:
            plt.rcParams.update('font', **self.font)
        if self.font_size is not None:
            plt.rcParams.update('font.size', self.font_size)

        t_start = time()

        external_config = self._parse_external_configuration(self.config)

        for (ax, plt_config) in self.plots.items():
            if isinstance(plt_config, list):
                # If configuration is list
                # overlap different plot on same axes.
                for subplot_config in plt_config:
                    try:
                        self._plot(ax, subplot_config, external_config, self.data)
                    except RuntimeError as error:
                        print(error)
                        continue
            else:
                self._plot(ax, plt_config, external_config, self.data)

        if save is not None:
            save = Path(save)
            self.fig.savefig(save)

            print(
                f'Plot complete in {time()-t_start:.4f} second.\n'
                f'Figure output to {save.absolute()}\n'
            )
        else:
            plt.show()

    def _parse_external_configuration(self, config) -> Dict[str, Any]:
        if isinstance(config, list):
            result = {}
            for sub_config in config:
                result = {
                    **result,
                    **(self._parse_external_configuration(sub_config))
                }

        if isinstance(config, str):
            config = Path(config)

        if isinstance(config, PathLike):
            with open(config) as fp:
                return yaml.load(fp, Loader=yaml.SafeLoader)

        if isinstance(config, dict):
            return config

        return {}

    def _plot(self, ax, plt_config, external_config, data):
        plt_type, plt_data, plt_args = plt_config.parse(
            external_config, data
        )

        if isinstance(plt_type, str):
            if plt_type in plot_manager.plots():
                print(f'Plotting {plt_type}...')
                plot_manager.plot(plt_type)(ax, plt_data, **plt_args)
            else:
                raise RuntimeError(f'Plot definition not found: {plt_type}. Skip.')
        else:
            print(f'Plotting {plt_type.name}...')
            plt_type(ax, plt_data, **plt_args)

    def __getitem__(self, ax):
        return self.plots[ax]

    def __setitem__(self, ax, value):
        self.plots[ax] = value
