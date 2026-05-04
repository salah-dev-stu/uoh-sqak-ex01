# Sequence — `sdk.train_model(arch, bundle, seed)`

```
  CLI                SDK             TrainingService    Registry      TrainingLoop      EvaluationService
   |                  |                    |              |                 |                   |
   |--train()-------->|                    |              |                 |                   |
   |                  |--train()---------->|              |                 |                   |
   |                  |                    |--build()---->|                 |                   |
   |                  |                    |              |--FCExtractor---|                   |
   |                  |                    |--build_optimizer()->Adam      |                   |
   |                  |                    |--SinusoidWindowDataset (FC view)                  |
   |                  |                    |              |                 |                   |
   |                  |                    |--TrainingLoop(model,...)------>|                   |
   |                  |                    |              |                 |--epoch loop ----->|
   |                  |                    |              |                 |  (train→val)      |
   |                  |                    |              |                 |  (hook fire)      |
   |                  |                    |              |                 |  (early stop)     |
   |                  |                    |              |                 |--TrainingResult-->|
   |                  |                    |--persist loss_history.json                         |
   |                  |                    |--persist best_model.pt                             |
   |                  |--RunHandle---------|              |                 |                   |
   |<--RunHandle------|                    |              |                 |                   |
   |                  |                    |              |                 |                   |
   |--evaluate()----->|                    |              |                 |                   |
   |                  |--evaluate()----------------------------------------->|                   |
   |                  |                    |              |              eval()                 |
   |                  |                    |              |              read model_cfg from JSON|
   |                  |                    |              |              load best_model.pt     |
   |                  |                    |              |              compute metrics        |
   |                  |                    |              |              persist eval_report    |
   |                  |<--EvalReport------------------------------------------------------------|
   |<--EvalReport-----|                    |              |                 |                   |
```
