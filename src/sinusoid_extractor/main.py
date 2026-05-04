"""Thin CLI wrapper around :class:`SinusoidExtractorSDK`. No business logic here."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from sinusoid_extractor.constants import Architecture
from sinusoid_extractor.sdk.sdk import SinusoidExtractorSDK
from sinusoid_extractor.shared.logger import configure_logging
from sinusoid_extractor.shared.version import __version__

_log = logging.getLogger("sinusoid_extractor.cli")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sinusoid-extractor", description="HW1 SDK CLI")
    p.add_argument("--config", type=Path, default=None, help="path to setup.json")
    p.add_argument("--log-level", default="INFO")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate-data", help="generate one dataset")
    g.add_argument("--alpha", type=float, required=True)
    g.add_argument("--seed", type=int, default=None)

    t = sub.add_parser("train", help="train one model")
    t.add_argument("--arch", choices=[a.value for a in Architecture], required=True)
    t.add_argument("--alpha", type=float, required=True)
    t.add_argument("--seed", type=int, default=None)

    sub.add_parser("run-matrix", help="run the full experiment matrix")
    sub.add_parser("run-oat", help="run the OAT sensitivity sweep")
    sub.add_parser("version", help="print version and exit")
    sub.add_parser("health", help="print SDK self-diagnostic")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging()
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

    if args.cmd == "version":
        print(__version__)
        return 0

    sdk = SinusoidExtractorSDK(config_path=args.config)

    if args.cmd == "health":
        for key, val in sdk.health_check().items():
            print(f"{key}: {val}")
        return 0

    if args.cmd == "generate-data":
        bundle = sdk.generate_dataset(alpha=args.alpha, seed=args.seed)
        _log.info("dataset summary: %s", bundle.summary())
        return 0

    if args.cmd == "train":
        bundle = sdk.generate_dataset(alpha=args.alpha, seed=args.seed)
        handle = sdk.train_model(arch=args.arch, bundle=bundle, seed=args.seed)
        report = sdk.evaluate(handle, bundle)
        _log.info("run_id=%s test_mse=%.6f", handle.run_id, report.test_mse)
        return 0

    if args.cmd == "run-matrix":
        handles = sdk.run_experiment_matrix()
        _log.info("matrix completed: %d runs", len(handles))
        return 0

    if args.cmd == "run-oat":
        handles = sdk.run_oat_sweep()
        _log.info("oat completed: %d runs", len(handles))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
