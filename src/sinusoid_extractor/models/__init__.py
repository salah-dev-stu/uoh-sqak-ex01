"""Model package. Importing this module auto-registers FC / RNN / LSTM.

Add a new architecture by creating a new file in this directory that decorates
its class with `@register("name")`. Do not edit existing model files when
extending.
"""

from sinusoid_extractor.models import fc_model, lstm_model, rnn_model  # noqa: F401
from sinusoid_extractor.models.registry import ModelRegistry

__all__ = ["ModelRegistry"]
