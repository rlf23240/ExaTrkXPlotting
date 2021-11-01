#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union, Dict, List, Any, AnyStr
from os import PathLike
from pathlib import Path
from time import time

import yaml

from matplotlib.axes import Axes
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from .plot_config import PlotConfig


class _Plotter:
    def __init__(self):
        self.plots = {}

    def plot(self, name, data_req: List = None):
        """
        Decoration to define a plot.

        :param name:
            Type name of this plot. Use in all configurations plot_figure.
        :param data_req:
            Data requirements.
            This will be use to check input data before plotting.
            Only work if data is subscriptable.
            None if you want to disable this feature.
        :return:
            Decorator.
        """
        def decorator(func):
            if data_req is not None:
                # If data check is enable, wrap func with checking.
                def wrapper(ax, data, **kwargs):
                    for requirement in data_req:
                        if requirement not in data:
                            raise RuntimeError(
                                f'Data requirement for {name} not satisfy: {requirement}'
                            )
                    func(ax, data, **kwargs)
            else:
                wrapper = func

            self.plots[name] = wrapper

            return wrapper

        return decorator

    def plot_figure(
        self,
        fig: Figure,
        axes: Dict[Axes, Union[PlotConfig, List[PlotConfig]]],
        config: Any = None,
        data: Any = None,
        save: Union[PathLike, AnyStr] = None
    ):
        """
        Plot a figure.

        :param fig:
            matplotlib Figure object.
        :param axes:
            Configurations define how to plot each axes.
        :param config:
            Single or list of external configuration file path or config dict.
        :param data:
            Data pass to all plotting function if no data assign in configuration.
        :param save:
            Figure save location. None if you want to show plot instead of save it.
        :return:
        """
        t_start = time()

        external_config = self._parse_external_configuration(config)

        for (ax, plt_config) in axes.items():
            if isinstance(plt_config, list):
                # If configuration is list
                # overlap different plot on same axes.
                for subplot_config in plt_config:
                    try:
                        self._plot(ax, subplot_config, external_config, data)
                    except RuntimeError as error:
                        print(error)
                        continue
            else:
                self._plot(ax, plt_config, external_config, data)

        if save is not None:
            save = Path(save)
            fig.savefig(save)

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
            if plt_type in self.plots:
                print(f'Plotting {plt_type}...')
                self.plots[plt_type](ax, plt_data, **plt_args)
            else:
                raise RuntimeError(f'Plot definition not found: {plt}. Skip.')
        else:
            print(f'Plotting {plt_type.__name__}...')
            plt_type(ax, plt_data, **plt_args)


_plotter = _Plotter()


def plots() -> List[str]:
    """
    Get current defined plots.

    :return: List of defined plots.
    """
    return list(_plotter.plots.keys())


def plot(name, data_req: List = None):
    """
    Decoration to define a plot.

    A plot must have function signature (ax, data, kwargs...)

    :param name:
        Type name of this plot. Use in all configurations plot_figure.
    :param data_req:
        Data requirements.
        This will be use to check input data before plotting.
        Only work if data object support `in` operation.
        None if you want to disable this feature.
    :return:
        Decorator.
    """
    return _plotter.plot(name, data_req)


def plot_figure(
    fig: Figure,
    axes: Dict[Axes, Union[PlotConfig, List[PlotConfig]]],
    config: Union[PathLike, AnyStr] = None,
    data: Any = None,
    save: Union[PathLike, AnyStr] = None
):
    """
    Plot a figure.

    :param fig:
        matplotlib Figure object.
    :param axes:
        Configurations define how to plot each axes.
    :param config:
        Single or list of external configuration file path or config dict.
    :param data:
        Data pass to all plotting function if no data assign in configuration.
    :param save:
        Figure save location. None if you want to show plot instead of save it.
    :return:
    """
    return _plotter.plot_figure(fig, axes, config, data, save=save)
