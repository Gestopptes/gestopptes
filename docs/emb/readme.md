# Using Embedding Models for Semantic Search

When selecting an embedding model for a retrieval-augmented generation (RAG) system, several criteria must be considered. Here are key characteristics to keep in mind when choosing such a model:

1. **Context Size**: Embedding models have a significantly smaller maximum context size compared to large language models (LLMs).
2. **Embedding Dimension**: This represents the amount of information encoded in the embedding.
3. **Model Size**: Recent embedding models that are larger in size are more expensive per million tokens.
4. **MaaS vs. Self-Hosted**: Depending on cost constraints, models can be used as a service (MaaS) or hosted locally.

## Context Size

Embedding models typically handle context sizes ranging from hundreds to thousands, or at most tens of thousands, of tokens. In contrast, LLMs can manage context sizes that are tens or hundreds of times larger. This difference is significant for the number of document chunks that can be returned by the semantic search component.

For self-hosted embedding models, the context size refers to the training context size. Some self-hosted models can run with any context size, but the quality of the vector representation may degrade with larger contexts. The number of tokens in the embedding model's context should be chosen based on the data ingestion system's needs, the type and structure of the ingested documents, and the query size used in semantic searches. There should be a proportional relationship between these factors. For example, using short queries (simple questions) at runtime requires finer document splitting during data ingestion. Conversely, using long queries (detailed descriptions or search templates) at runtime necessitates a larger context during data ingestion.

### Ideal Context

Ideally, each chunk should contain a single idea or component of an idea. However, such precise division is often too difficult or costly. Therefore, document splitting techniques rely either on the intrinsic properties of structured or semi-structured texts or on the temporal correlation of similar ideas using a sliding window approach. In practice, combining these two techniques yields the best results: first, splitting based on structure, followed by sliding window division to ensure consistent chunk sizes.

## Embedding Dimension

The embedding vector can encompass hundreds or thousands of abstract features. There is a clear proportional relationship between the embedding dimension, the model's context size, and the model size itself. The embedding dimension also represents the amount of information the model can encode.

For a semantic search system where both the chunk and the query are short, a model with a smaller embedding dimension might be sufficient. In contrast, for a system based on templates, using a larger model becomes necessary to encode more information.

## Model Size

Model size can be a hurdle for running self-hosted or on-device models. Larger models require GPUs for sufficient throughput, whereas only smaller models can run on CPUs. Larger models also need GPUs with more VRAM, increasing infrastructure and per-token costs.

The end-to-end results of a RAG system depend on the embedding model, which operates in parallel with the LLM. Regardless of how good the LLM becomes, if it does not receive the necessary context, it will hallucinate. However, you can work around a small embedding model by engineering a better retrieval system, using relevance filtering, multiple embedding levels, or specific preprocessing for document chunking based on the use case.

## MaaS vs. Self-Hosted

Embedding models are easy to host locally. Depending on the data ingestion volume and speed requirements, these models can run as REST APIs over CPUs/GPUs or on devices.

For ingesting large amounts of data, self-hosted embedding models can be a viable solution to reduce costs and overcome usage limits imposed by some providers. Not all embedding models have open weights, so if self-hosting is desired, the model must be chosen from the available pool. However, through platforms like Huggingface, there are solutions for almost all needs regarding model size, vector size, or context size.

## Conclusion

I recommend starting any project with a small embedding model in terms of size, context, and vector, especially if ingesting tens of gigabytes of natural language data. If documents cannot be split into small chunks or if the semantic understanding level of the context is insufficient for the developed system, use the most powerful model available. If the powerful model is sufficient, optimize costs by finding the smallest model that still works in the system. If even the most powerful model is insufficient, the problem lies in the approach. Hierarchical use of embeddings can bring the desired improvements, possibly at a reduced cost.