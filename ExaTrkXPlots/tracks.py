#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plots about particle tracks in ExaTrkX routine.

For plot data requirement, detail list below:
    - generated:
        Generated tracks.

    - reconstructable:
        Reconstructable tracks.

    - matched:
        Matched tracks

No required column for those dataframes, but if you assign x_variable or track_filter,
then used column must exist.
"""

from typing import Callable
import math

import numpy as np

from ExaTrkXPlotting import plot


@plot('exatrkx.tracks.distribution', ['generated', 'reconstructable', 'matched'])
def tracks(
    ax,
    data,
    x_variable,
    x_label,
    bins,
    track_filter: Callable = None,
    log_scale: bool = False
):
    """
    Plot track histogram.

    :param ax: matplotlib axis object.
    :param data: Data. Must contain column used in x_variable and track_filter.
    :param x_variable: X axis of distribution. Must exist in data.
    :param x_label: X label string.
    :param bins: Bins of histogram.
    :param track_filter: Plot track pass filter only.
    :param log_scale: Enable log scale.
    :return:
    """
    generated = data['generated']
    reconstructable = data['reconstructable']
    matched = data['matched']

    # Apply filter.
    if track_filter is not None:
        generated = generated[track_filter(generated)]
        reconstructable = reconstructable[track_filter(reconstructable)]
        matched = matched[track_filter(matched)]

    ax.hist(
        generated[x_variable],
        label='Generated',
        histtype='step',
        lw=2,
        log=log_scale,
        bins=bins,
    )
    ax.hist(
        reconstructable[x_variable],
        label='Reconstructable',
        histtype='step',
        lw=2,
        log=log_scale,
        bins=bins
    )
    ax.hist(
        matched[x_variable],
        label='Matched',
        histtype='step',
        lw=2,
        log=log_scale,
        bins=bins
    )

    ax.set_ylabel('Events')
    ax.set_xlabel(x_label)

    ax.legend()
    ax.grid(True)


def _efficiency(matched, population):
    """
    Helper function to generate efficiency and statistical error for each bins.

    :param matched: Number of matched classification in each bins.
    :param population: Population in each bins.
    :return: Efficiency, Error
    """

    efficiency = [
        x / y if y != 0 else 0.0 for x, y in zip(
            matched, population
        )
    ]
    error = [
        math.sqrt(eff * (1.0 - eff) / y) if y != 0 else 0.0 for eff, y in zip(
            efficiency, population
        )
    ]

    return efficiency, error


@plot('exatrkx.tracks.efficiency', ['generated', 'reconstructable', 'matched'])
def tracking_efficiency(ax, data, x_variable, x_label, bins, track_filter=None):
    """
    Plot track efficiency, both physical and technical, define as

    Physical Efficiency = #Matched / #Generated

    Technical Efficiency = #Matched / #Reconstructable

    :param ax: matplotlib axis object.
    :param data: Data. Must contain column used in x_variable and track_filter.
    :param x_variable: X axis of distribution. Must exist in data.
    :param x_label: X label string.
    :param bins: Bins of histogram.
    :param track_filter: Plot track pass filter only.
    :return:
    """

    generated = data['generated']
    reconstructable = data['reconstructable']
    matched = data['matched']

    # Apply filter.
    if track_filter is not None:
        generated = generated[track_filter]
        reconstructable = reconstructable[track_filter]
        matched = matched[track_filter]

    # Compute histogram.
    gen_hist, gen_bins = np.histogram(generated[x_variable], bins=bins)
    reco_hist, reco_bins = np.histogram(reconstructable[x_variable], bins=bins)
    matched_hist, matched_bins = np.histogram(matched[x_variable], bins=bins)

    # Compute x location and error for each bin.
    xvals, xerrs = [], []
    for i in range(1, len(gen_bins)):
        xvals.append(0.5*(gen_bins[i]+gen_bins[i-1]))
        xerrs.append(0.5*(gen_bins[i]-gen_bins[i-1]))

    # Compute efficiency.
    physical_efficiency, physical_efficiency_error = _efficiency(
        matched_hist, gen_hist
    )
    technical_efficiency, technical_efficiency_error = _efficiency(
        matched_hist, reco_hist
    )

    ax.set_ylim(0.0, 1.0)

    # Plot physical and technical efficiency.
    ax.set_ylim(0.0, 1.0)
    ax.errorbar(
        xvals, physical_efficiency,
        xerr=xerrs, yerr=physical_efficiency_error,
        fmt='o', lw=2, label='Physical Efficiency'
    )
    ax.errorbar(
        xvals, technical_efficiency,
        xerr=xerrs, yerr=technical_efficiency_error,
        fmt='o', lw=2, label='Technical Efficiency'
    )

    if x_label is not None:
        ax.set_xlabel(x_label)

    ax.legend()
    ax.grid(True)


@plot('exatrkx.tracks.efficiency.technical', ['generated', 'reconstructable', 'matched'])
def tracking_efficiency_techical(
    ax,
    data,
    x_variable,
    x_label,
    bins,
    track_filter: Callable = None,
    label: str = None
):
    """
    Plot techical tracking efficiency, define as

    Technical Efficiency = #Matched / #Reconstructable

    :param ax: matplotlib axis object.
    :param data: Data. Must contain column used in x_variable and track_filter.
    :param x_variable: X axis of distribution. Must exist in data.
    :param x_label: X label string.
    :param bins: Bins of histogram.
    :param track_filter: Plot track pass filter only.
    :return:
    """

    generated = data['generated']
    reconstructable = data['reconstructable']
    matched = data['matched']

    # Apply filter.
    if track_filter is not None:
        generated = generated[track_filter(generated)]
        reconstructable = reconstructable[track_filter(reconstructable)]
        matched = matched[track_filter(matched)]

    # Compute histogram.
    gen_hist, gen_bins = np.histogram(generated[x_variable], bins=bins)
    reco_hist, reco_bins = np.histogram(reconstructable[x_variable], bins=bins)
    matched_hist, matched_bins = np.histogram(matched[x_variable], bins=bins)

    # Compute x location and error for each bin.
    xvals, xerrs = [], []
    for i in range(1, len(gen_bins)):
        xvals.append(0.5*(gen_bins[i]+gen_bins[i-1]))
        xerrs.append(0.5*(gen_bins[i]-gen_bins[i-1]))

    # Compute efficiency.
    technical_efficiency, technical_efficiency_error = _efficiency(
        matched_hist, reco_hist
    )

    # Plot technical efficiency.
    ax.set_ylim(0.0, 1.0)
    ax.errorbar(
        xvals, technical_efficiency,
        xerr=xerrs, yerr=technical_efficiency_error,
        fmt='o', lw=2, label=label
    )

    if x_label is not None:
        ax.set_xlabel(x_label)

    ax.legend()
    ax.grid(True)


@plot('exatrkx.tracks.efficiency.physical', ['generated', 'reconstructable', 'matched'])
def tracking_efficiency_physical(
    ax,
    data,
    x_variable,
    x_label,
    bins,
    track_filter: Callable = None,
    label: str = None
):
    """
    Plot physical tracking efficiency, define as

    Physical Efficiency = #Matched / #Generated

    :param ax: matplotlib axis object.
    :param data: Data. Must contain column used in x_variable and track_filter.
    :param x_variable: X axis of distribution. Must exist in data.
    :param x_label: X label string.
    :param bins: Bins of histogram.
    :param track_filter: Plot track pass filter only.
    :return:
    """

    generated = data['generated']
    reconstructable = data['reconstructable']
    matched = data['matched']

    # Apply filter.
    if track_filter is not None:
        generated = generated[track_filter(generated)]
        reconstructable = reconstructable[track_filter(reconstructable)]
        matched = matched[track_filter(matched)]

    # Compute histogram.
    gen_hist, gen_bins = np.histogram(generated[x_variable], bins=bins)
    reco_hist, reco_bins = np.histogram(reconstructable[x_variable], bins=bins)
    matched_hist, matched_bins = np.histogram(matched[x_variable], bins=bins)

    # Compute x location and error for each bin.
    xvals, xerrs = [], []
    for i in range(1, len(gen_bins)):
        xvals.append(0.5*(gen_bins[i]+gen_bins[i-1]))
        xerrs.append(0.5*(gen_bins[i]-gen_bins[i-1]))

    # Compute efficiency.
    physical_efficiency, physical_efficiency_error = _efficiency(
        matched_hist, gen_hist
    )

    # Plot physical efficiency.
    ax.set_ylim(0.0, 1.0)
    ax.errorbar(
        xvals, physical_efficiency,
        xerr=xerrs, yerr=physical_efficiency_error,
        fmt='o', lw=2, label=label
    )

    if x_label is not None:
        ax.set_xlabel(x_label)

    ax.legend()
    ax.grid(True)
