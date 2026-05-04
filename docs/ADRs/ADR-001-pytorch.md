# ADR-001 — PyTorch over TensorFlow

**Status**: Accepted (2026-05-04)

## Context
The lecturer's RNN book uses PyTorch idiom (`torch.nn.RNN`); the LSTM book references both, with PyTorch first. The course community uses PyTorch.

## Decision
Use PyTorch as the sole deep-learning framework.

## Consequences
- Free `torch.nn.RNN` and `torch.nn.LSTM` cells; well-tested Adam optimizer; `DataLoader` for parallel data loading.
- No keras-style symbolic API (which we don't need for this regression problem).
- Smaller install footprint than TensorFlow; faster `uv sync` on macOS.

## Alternatives considered
- **TensorFlow / Keras**: rejected — heavier dep, less aligned with course materials.
- **JAX**: rejected — overkill for this problem size; learning curve doesn't pay off in a 3-day project.
