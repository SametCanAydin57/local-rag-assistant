# Test Results

## Answerable Questions

| Question | Expected | Actual | Result |
|---|---|---|---|
| What is RAG? | Definition of RAG | Correct explanation using retrieved documents | ✅ |
| What is vector search? | Explanation of semantic similarity | Correct explanation using vector_search.txt | ✅ |
| What is SQLite used for? | Database explanation | Correct explanation using sqlite.txt | ✅ |


## Unanswerable Questions

| Question | Expected | Actual | Result |
|---|---|---|---|
| Who is Elon Musk? | I don't know | I don't know based on the provided documents | ✅ |
| What is quantum physics? | I don't know | I don't know based on the provided documents | ✅ |


## Edge Cases

| Question | Expected | Actual | Result |
|---|---|---|---|
| Empty input | Handle gracefully | Asked user to enter a question without crashing | ✅ |
| hi | Should not hallucinate an answer | No relevant documents found | ✅ |
| aaaaaaaaa | No crash | No relevant documents found | ✅ |


# Performance Evaluation

The application was tested locally using Microsoft Foundry Local.

## Response Time Analysis

Average response time was measured by separating the pipeline stages.

Example:

Query: "What is RAG?"

Results:

- Load embeddings: 0.01 seconds
- Query embedding generation: 2.53 seconds
- Retrieval: 0.00 seconds
- LLM generation: 12.09 seconds
- Total response time: 14.63 seconds

The evaluation shows that retrieval operations are efficient. Most of the latency comes from local LLM inference using Phi-3.5 Mini.

## Optimization Discussion

The retrieval process is already efficient because SQLite lookup and cosine similarity calculation take negligible time.

The main performance limitation is local LLM generation using Phi-3.5 Mini. Possible improvements include:

- Using a smaller language model for faster inference.
- Reducing the amount of retrieved context.
- Caching embeddings to avoid repeated computation.
- Using optimized vector databases for larger datasets.

# Evaluation Summary

The system successfully performs end-to-end RAG operations:

- Documents are converted into embeddings.
- Relevant information is retrieved using semantic similarity.
- Answers are generated using a local LLM.
- Unsupported questions are rejected.
- Source documents are displayed with similarity scores.

The main limitation is response latency caused by local LLM inference.