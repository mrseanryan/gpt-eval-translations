# gpt-eval-translations

Evaluate translations via either a self-hosted Embedder or using Chat-GPT.

- (self-hosted) Evaluate translations [via a local SBERT embedder](./src/eval-via-embedder/README.md)
- (self-hosted) Evaluate translations [via a local multi-lingual sentence embedder](./src/eval-via-multi-lingual-embedder/README.md)
- (remote) Evaluate translations with LLM as Judge [via Chat-GPT](./src/eval-via-chat-gpt/README.md)

The evaluator can be used as part of a machine learning pipeline, such as EPE (Extract, Predict, Evaluate) - [read more on Medium](https://medium.com/p/53999ff93dc4).

## Test utils

- [tmx to CSV converter](./src/test-util/README.md)
