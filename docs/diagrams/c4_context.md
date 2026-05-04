# C4 — System Context

```
        +------------------+
        |   Salah Qadah    |  <-- researcher (human)
        +--------+---------+
                 |
                 | runs CLI / opens notebook
                 v
       +-------------------+        reads results
       | Sinusoid          | <-----------------+
       | Extractor System  | -----------------+|
       +-------------------+ writes artefacts ||
                 |                            ||
                 | imports                    ||
                 v                            ||
        +------------------+                  ||
        |  PyTorch + NumPy |                  ||
        |  + SciPy stack   |                  ||
        +------------------+                  ||
                                              ||
        (No external API; no DB; no service.) ||
```

The system is single-process, single-machine, batch-oriented. No remote call, no auth, no concurrency beyond `DataLoader(num_workers)`.
