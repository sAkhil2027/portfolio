import subprocess
import os
import sys

os.chdir("f:/portfolio")

commits = [
    # 1. Environment configuration
    ([".env.example"], "feat(env): update environment configuration example for LLM and Groq API keys"),
    
    # 2. Embeddings resilience
    (["rag/embeddings/embedder.py"], "refactor(embeddings): add lightweight feature hashing and memory protection fallback"),
    
    # 3. Qdrant resilience
    (["rag/retrieval/qdrant.py"], "refactor(retrieval): enhance Qdrant retrieval resilience and connection handling"),
    
    # 4. Pipeline candidate pool
    (["rag/pipeline.py"], "feat(pipeline): expand candidate retrieval pool for cross-encoder reranking"),
    
    # 5. Chatbot package root
    (["chatbot/__init__.py"], "feat(chatbot): initialize Phase 4 chatbot package root"),
    
    # 6. Chatbot models package root
    (["chatbot/models/__init__.py"], "feat(models): initialize chatbot models package root"),
    
    # 7. ChatRequest schema
    (["chatbot/models/request.py"], "feat(models): add ChatRequest schema with dual-key aliases and length guardrails"),
    
    # 8. ChatResponse & Citation schemas
    (["chatbot/models/response.py"], "feat(models): add ChatResponse and Citation structured schemas"),
    
    # 9. Query package root
    (["chatbot/query/__init__.py"], "feat(query): initialize query processing package root"),
    
    # 10. QueryProcessor with follow-up rewriting
    (["chatbot/query/processor.py"], "feat(query): implement QueryProcessor with zero-latency follow-up rewriting"),
    
    # 11. Context package root
    (["chatbot/context/__init__.py"], "feat(context): initialize context builder package root"),
    
    # 12. ContextBuilder with deduplication
    (["chatbot/context/builder.py"], "feat(context): implement ContextBuilder with near-duplicate text deduplication"),
    
    # 13. Prompts package root
    (["chatbot/prompts/__init__.py"], "feat(prompts): initialize system prompt package root"),
    
    # 14. SystemPromptBuilder
    (["chatbot/prompts/system.py"], "feat(prompts): add SystemPromptBuilder with persona and anti-injection secrecy rule"),
    
    # 15. LLM package root
    (["chatbot/llm/__init__.py"], "feat(llm): initialize LLM client package root"),
    
    # 16. LLMClient multi-provider
    (["chatbot/llm/client.py"], "feat(llm): implement multi-provider LLMClient supporting Free Groq Cloud and Gemini"),
    
    # 17. Safety package root
    (["chatbot/safety/__init__.py"], "feat(safety): initialize safety and validation package root"),
    
    # 18. AnswerValidator guardrails
    (["chatbot/safety/validator.py"], "feat(safety): add AnswerValidator with empty response defense and length caps"),
    
    # 19. IP RateLimiter
    (["chatbot/safety/rate_limiter.py"], "feat(safety): implement in-memory sliding-window IP RateLimiter"),
    
    # 20. Streaming package root
    (["chatbot/streaming/__init__.py"], "feat(streaming): initialize SSE streaming package root"),
    
    # 21. SSEFormatter
    (["chatbot/streaming/sse.py"], "feat(streaming): implement SSEFormatter for structured event-based token streams"),
    
    # 22. ChatbotService
    (["chatbot/service.py"], "feat(service): add ChatbotService master orchestrator with early no-context bypass and telemetry"),
    
    # 23. Chat API routes
    (["app/routes/chat.py"], "feat(api): implement POST /api/chat and POST /api/chat/stream endpoints with rate limiting"),
    
    # 24. FastAPI app factory
    (["app/__init__.py"], "feat(server): mount chat router and register RAG lifespan pipeline in application factory"),
    
    # 25. Uvicorn startup
    (["app/main.py"], "fix(server): enhance Uvicorn worker reload handling for Windows environments"),
    
    # 26. Page routes & health check
    (["app/routes/pages.py"], "refactor(pages): enhance health check endpoint and error diagnostics"),
    
    # 27. Client JavaScript streaming
    (["app/static/js/chat.js"], "feat(ui): add vanilla JS Server-Sent Events streaming client"),
    
    # 28. CSS Glassmorphism styling
    (["app/static/css/style.css"], "feat(ui): add modern Dark Glassmorphism styles and animations for Chatbot widget"),
    
    # 29. Base HTML template
    (["app/templates/base.html"], "feat(ui): integrate floating Chatbot modal and clear chat action in base template"),
    
    # 30. Test environment
    (["tests/test_environment.py"], "test(env): add test_environment suite for configuration verification"),
    
    # 31. Chat evaluation dataset
    (["tests/chat_evaluation.json"], "test(eval): create chat_evaluation.json benchmark scenarios dataset"),
    
    # 32. Chatbot unit test suite
    (["tests/test_chatbot.py"], "test(chatbot): add unit test suite for request validation, streaming, and safety"),
    
    # 33. API integration tests
    (["tests/test_api.py"], "test(api): update API integration test suite for chat endpoints"),
    
    # 34. Qdrant tests & scratch tools
    (["tests/test_qdrant.py"], "test(qdrant): update Qdrant vector retrieval test suite")
]

print(f"Total commits planned: {len(commits)}")

for idx, (files, msg) in enumerate(commits, 1):
    for f in files:
        if os.path.exists(f):
            subprocess.run(["git", "add", f], check=True)
    res = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    print(f"[{idx}/34] {msg} -> {res.returncode}")
    if res.returncode != 0 and "nothing to commit" not in res.stderr and "nothing to commit" not in res.stdout:
        print(f"Error on commit {idx}: {res.stderr} {res.stdout}")
