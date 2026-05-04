"""Regression metrics — pure-numpy, dtype-agnostic."""

from __future__ import annotations

import math

import numpy as np
import torch

ArrayLike = np.ndarray | torch.Tensor


def _as_numpy(a: ArrayLike) -> np.ndarray:
    if isinstance(a, torch.Tensor):
        return a.detach().cpu().numpy()
    return np.asarray(a)


def mse(pred: ArrayLike, target: ArrayLike) -> float:
    p, t = _as_numpy(pred), _as_numpy(target)
    if p.shape != t.shape:
        raise ValueError(f"shape mismatch: {p.shape} vs {t.shape}")
    if p.size == 0:
        return float("nan")
    return float(np.mean((p - t) ** 2))


def mae(pred: ArrayLike, target: ArrayLike) -> float:
    p, t = _as_numpy(pred), _as_numpy(target)
    if p.shape != t.shape:
        raise ValueError(f"shape mismatch: {p.shape} vs {t.shape}")
    if p.size == 0:
        return float("nan")
    return float(np.mean(np.abs(p - t)))


def r2_score(pred: ArrayLike, target: ArrayLike) -> float:
    p, t = _as_numpy(pred), _as_numpy(target)
    if p.shape != t.shape:
        raise ValueError(f"shape mismatch: {p.shape} vs {t.shape}")
    if p.size == 0:
        return float("nan")
    ss_res = float(np.sum((t - p) ** 2))
    ss_tot = float(np.sum((t - t.mean()) ** 2))
    if ss_tot == 0.0:
        return 0.0
    return 1.0 - ss_res / ss_tot


def snr_db(pred: ArrayLike, target: ArrayLike) -> float:
    p, t = _as_numpy(pred), _as_numpy(target)
    if p.shape != t.shape:
        raise ValueError(f"shape mismatch: {p.shape} vs {t.shape}")
    signal_power = float(np.sum(t**2))
    error_power = float(np.sum((p - t) ** 2))
    if error_power == 0.0:
        return math.inf
    if signal_power == 0.0:
        return -math.inf
    return 10.0 * math.log10(signal_power / error_power)


def predict_zero_baseline(target: ArrayLike) -> float:
    """MSE of the constant ``yhat = 0`` predictor — sanity floor."""
    t = _as_numpy(target)
    if t.size == 0:
        return float("nan")
    return float(np.mean(t**2))
