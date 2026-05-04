# C4 — Container Diagram

```
   +------------------------------+      +-------------------------------+
   |  CLI Container               |      |  Jupyter Notebook Container   |
   |  python -m sinusoid_extractor|      |  notebooks/analysis.ipynb     |
   |  (argparse → SDK calls)      |      |  (LaTeX + plots + Wilcoxon)   |
   +-------------+----------------+      +---------------+---------------+
                 |                                       |
                 | calls SDK                             | calls SDK
                 v                                       v
   +-----------------------------------------------------------------+
   |   SDK Container (src/sinusoid_extractor/sdk/sdk.py)             |
   |   class SinusoidExtractorSDK                                    |
   |     .generate_dataset(...)                                      |
   |     .train_model(arch, hyperparams, dataset_id) -> RunHandle    |
   |     .evaluate(run_id) -> EvalReport                             |
   |     .run_experiment_matrix(...)                                 |
   |     .run_oat_sweep(...)                                         |
   +-----+--------+--------+----------+----------+--------+----------+
         |        |        |          |          |        |
         v        v        v          v          v        v
      Dataset Training Evaluation  Model      Config  Gatekeeper
      Service  Service  Service    Registry   Loader  (no-op stub)
         |        |        |          |          |        |
         v        v        v          v          v        v
   +-------------------------------------------------------+
   |              Filesystem (data/, results/, config/)    |
   +-------------------------------------------------------+
```
