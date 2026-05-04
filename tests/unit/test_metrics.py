"""Tests for ``services.metrics``."""

import math

import numpy as np
import pytest
import torch

from sinusoid_extractor.services import metrics as m


def test_mse_zero_for_identical() -> None:
    a = np.array([1.0, 2.0, 3.0])
    assert m.mse(a, a) == 0.0


def test_mae_zero_for_identical() -> None:
    a = np.array([1.0, 2.0])
    assert m.mae(a, a) == 0.0


def test_r2_perfect_prediction_is_one() -> None:
    a = np.array([1.0, 2.0, 3.0, 4.0])
    assert m.r2_score(a, a) == 1.0


def test_r2_constant_target_handled() -> None:
    a = np.array([1.0, 1.0, 1.0])
    assert m.r2_score(np.array([1.0, 1.0, 1.0]), a) == 0.0


def test_r2_can_be_negative() -> None:
    target = np.array([1.0, 2.0, 3.0])
    pred = np.array([3.0, 2.0, 1.0])
    assert m.r2_score(pred, target) < 0.0


def test_snr_db_perfect_is_inf() -> None:
    a = np.array([1.0, 2.0])
    assert m.snr_db(a, a) == math.inf


def test_snr_db_zero_signal_is_neg_inf() -> None:
    pred = np.array([1.0, 2.0])
    target = np.array([0.0, 0.0])
    assert m.snr_db(pred, target) == -math.inf


def test_predict_zero_baseline() -> None:
    target = np.array([1.0, 2.0])
    assert m.predict_zero_baseline(target) == 2.5


def test_torch_input_supported() -> None:
    pred = torch.zeros(3)
    target = torch.zeros(3)
    assert m.mse(pred, target) == 0.0


def test_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        m.mse(np.zeros(3), np.zeros(4))


def test_empty_arrays_return_nan() -> None:
    assert math.isnan(m.mse(np.empty(0), np.empty(0)))
    assert math.isnan(m.mae(np.empty(0), np.empty(0)))
    assert math.isnan(m.r2_score(np.empty(0), np.empty(0)))
    assert math.isnan(m.predict_zero_baseline(np.empty(0)))
