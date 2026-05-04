"""Shared pytest fixtures."""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import pytest
import torch

from sinusoid_extractor.constants import DEFAULT_SEED


@pytest.fixture(autouse=True)
def _global_seed() -> None:
    """Seed Python / NumPy / PyTorch deterministically before every test."""
    random.seed(DEFAULT_SEED)
    np.random.seed(DEFAULT_SEED)
    torch.manual_seed(DEFAULT_SEED)


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(DEFAULT_SEED)


@pytest.fixture
def tiny_config_dict() -> dict:
    return {
        "version": "1.00",
        "dataset": {
            "frequencies_hz": [1, 3, 5, 7],
            "amplitude": 1.0,
            "sampling_rate_hz": 1000,
            "duration_seconds": 1.0,
            "context_window": 10,
            "n_train": 100,
            "n_val": 50,
            "n_test": 50,
            "seed": 42,
            "noise_levels_alpha": [0.05],
        },
        "training": {
            "optimizer": "adam",
            "learning_rate": 0.001,
            "batch_size": 16,
            "max_epochs": 2,
            "early_stopping_patience": 1,
            "num_workers": 0,
        },
        "models": {
            "fc": {"hidden_size": 16, "num_layers": 1, "dropout": 0.0},
            "rnn": {"hidden_size": 16, "num_layers": 1, "dropout": 0.0},
            "lstm": {"hidden_size": 16, "num_layers": 1, "dropout": 0.0},
        },
        "experiment": {
            "seeds": [42],
            "architectures": ["fc", "rnn", "lstm"],
            "target_frequency_indices": [0, 1, 2, 3],
        },
        "oat_sweep": {
            "hidden_size": [8],
            "num_layers": [1],
            "dropout": [0.0],
            "learning_rate": [0.001],
        },
        "paths": {"data_dir": "data", "results_dir": "results", "logs_dir": "logs"},
    }


@pytest.fixture
def tiny_config_path(tmp_path: Path, tiny_config_dict: dict) -> Path:
    p = tmp_path / "setup.json"
    p.write_text(json.dumps(tiny_config_dict, indent=2))
    return p


@pytest.fixture
def rate_limits_path(tmp_path: Path) -> Path:
    p = tmp_path / "rate_limits.json"
    p.write_text(json.dumps({
        "version": "1.00",
        "services": {
            "default": {
                "requests_per_minute": 30, "requests_per_hour": 500,
                "concurrent_max": 5, "retry_after_seconds": 30, "max_retries": 3,
            },
        },
    }))
    return p
