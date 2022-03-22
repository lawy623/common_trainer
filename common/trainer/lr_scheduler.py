# -*- coding: utf-8 -*-

import math

import numpy as np
import torch


def get_learning_rate_scheduler(
    optimizer, last_epoch=0, total_epoch=100, lr_scheduler='MultiStepLR', lr_gamma=0.1, lr_steps=[], **kwargs
):
    """Setup learning rate scheduler. Now support [MultiStepLR, ExponentialLR, PolyLR]. """
    if lr_scheduler == 'ExponentialLR':
        lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, lr_gamma, last_epoch=last_epoch)
    elif lr_scheduler == 'MultiStepLR':
        lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=lr_steps, gamma=lr_gamma, last_epoch=last_epoch
        )
    elif lr_scheduler == 'PolyLR':
        lr_gamma = math.log(0.1) / math.log(1 - (lr_steps[0] - 1e-6) / total_epoch)

        # Poly with lr_gamma until args.lr_milestones[0], then stepLR with factor of 0.1
        def lambda_map(epoch_index):
            return math.pow(1 - epoch_index / total_epoch, lr_gamma) \
                if np.searchsorted(lr_steps, epoch_index + 1) == 0 \
                else math.pow(10, -1 * np.searchsorted(lr_steps, epoch_index + 1))

        lr_scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda_map, last_epoch=last_epoch)

    else:
        raise NameError('Unknown {} learning rate scheduler'.format(lr_scheduler))

    return lr_scheduler
