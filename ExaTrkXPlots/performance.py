#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ExaTrkXPlotting import plotter

import sklearn.metrics


@plotter.plot('exatrkx.performance.score_distribution', ['truth', 'score'])
def score_distribution(
    ax,
    data,
    log_scale=True,
    bins=50,
    title=None
):
    """
    Plot score distribution for true and fake data.

    :param ax: matplotlib axis object.
    :param data: Data.
    :param log_scale: Enable log scale for y-axis.
    :param bins: Bins for histogram
    :param title: Plot title.
    :return:
    """
    score = data['score']

    # Truth should be bool array.
    # We apply >0.5 in case user pass numerical array.
    truth = (data['truth'] > 0.5)

    # True target.
    ax.hist(
        score[truth],
        bins=bins,
        log=log_scale,
        histtype='step',
        lw=2,
        label='true'
    )
    # False target.
    ax.hist(
        score[~truth],
        bins=bins,
        log=log_scale,
        histtype='step',
        lw=2,
        label='fake'
    )

    ax.set_xlabel('Model Output')
    ax.legend()

    if title is not None:
        ax.set_title(title)


@plotter.plot('exatrkx.performance.roc_curve', ['truth', 'score'])
def score_roc_curve(
    ax,
    data,
    title=None
):
    """
    Plot ROC curve.

    :param ax: matplotlib axis object.
    :param data: Data.
    :param title: Plot title. If None, "ROC curve, AUC = {auc:.4f}" will be used.
    :return:
    """
    score = data['score']

    # Truth should be bool array.
    # We apply >0.5 in case user pass numerical array.
    truth = (data['truth'] > 0.5)

    # Compute curve.
    if all(tag in data for tag in ['false_positive_rate', 'true_positive_rate']):
        # If user pass precompute precision, recall, thresholds,
        # we don't need to recompute all of them.
        false_positive_rate = data['false_positive_rate']
        true_positive_rate = data['true_positive_rate']
    else:
        # Compute curve.
        false_positive_rate, true_positive_rate, _ = sklearn.metrics.roc_curve(truth, score)

    auc = sklearn.metrics.auc(
        false_positive_rate,
        true_positive_rate
    )

    # ROC curve.
    ax.plot(
        false_positive_rate,
        true_positive_rate,
        lw=2
    )

    # AUC=0.5.
    ax.plot([0, 1], [0, 1], '--', lw=2)

    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.tick_params(width=2, grid_alpha=0.5)

    if title is None:
        # If no title, use AUC as title.
        ax.set_title(f'ROC curve, AUC = {auc:.4f}')
    else:
        ax.set_title(title)


@plotter.plot('exatrkx.performance.precision_recall_with_threshold', ['truth', 'score'])
def precision_recall_with_threshold(
    ax,
    data,
    title=None
):
    """
    Plot precision and recall change with different threshold.

    :param ax: matplotlib axis object.
    :param data: Data.
    :param title: Plot title.
    :return:
    """
    score = data['score']

    # Truth should be bool array.
    # We apply >0.5 in case user pass numerical array.
    truth = (data['truth'] > 0.5)

    # Compute curve.
    if all(tag in data for tag in ['precision', 'recall', 'thresholds']):
        # If user pass precompute precision, recall, thresholds,
        # we don't need to recompute all of them.
        precision = data['precision']
        recall = data['recall']
        thresholds = data['thresholds']
    else:
        # Compute curve.
        precision, recall, thresholds = sklearn.metrics.precision_recall_curve(
            truth,
            score
        )

    ax.plot(thresholds, precision[:-1], label='purity', lw=2)
    ax.plot(thresholds, recall[:-1], label='efficiency', lw=2)
    ax.set_xlabel('Cut on model score')
    ax.tick_params(width=2, grid_alpha=0.5)
    ax.legend(loc='upper right')

    if title is not None:
        ax.set_title(title)


@plotter.plot('exatrkx.performance.precision_recall', ['truth', 'score'])
def precision_recall_curve(
    ax,
    data,
    title=None
):
    """
    Plot precision and recall dependency.

    :param ax: matplotlib axis object.
    :param data: Data.
    :param title: Plot title.
    :return:
    """
    score = data['score']

    # Truth should be bool array.
    # We apply >0.5 in case user pass numerical array.
    truth = (data['truth'] > 0.5)

    if all(tag in data for tag in ['precision', 'recall']):
        # If user pass precompute precision, recall, thresholds,
        # we don't need to recompute all of them.
        precision = data['precision']
        recall = data['recall']
    else:
        # Compute curve.
        precision, recall, _ = sklearn.metrics.precision_recall_curve(
            truth,
            score
        )

    ax.plot(precision, recall, lw=2)
    ax.set_xlabel('Purity')
    ax.set_ylabel('Efficiency')
    ax.tick_params(width=2, grid_alpha=0.5)

    if title is not None:
        ax.set_title(title)
