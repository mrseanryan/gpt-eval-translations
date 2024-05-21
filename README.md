# gpt-eval-translations

Evaluate translations via either a self-hosted Embedder or using Chat-GPT.

- (self-hosted) Evaluate translations [via a local SBERT embedder](./src/eval-via-embedder/README.md)
- (remote) Evaluate translations with LLM as Judge [via Chat-GPT](./src/eval-via-chat-gpt/README.md)

The evaluator can be used as part of a machine learning pipeline, such as EPE (Extract, Predict, Evaluate) - [read more on Medium](https://medium.com/p/53999ff93dc4).
