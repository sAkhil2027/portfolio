"""
Chatbot Master Service module.
Orchestrates Phase 4 pipeline: Query Processing -> Phase 3 Retrieval -> Context & Prompt Assembly -> LLM Generation -> SSE Streaming.
Includes early no-context short-circuiting and structured latency telemetry logging.
"""

import time
import logging
from typing import AsyncGenerator, Dict, Any, Optional
from chatbot.models.request import ChatRequest
from chatbot.models.response import ChatResponse
from chatbot.query.processor import QueryProcessor
from chatbot.context.builder import ContextBuilder
from chatbot.prompts.system import SystemPromptBuilder
from chatbot.llm.client import LLMClient
from chatbot.safety.validator import AnswerValidator
from chatbot.streaming.sse import SSEFormatter

logger = logging.getLogger("chatbot.telemetry")


class ChatbotService:
    """
    Master Phase 4 Chatbot Service orchestrator with telemetry logging.
    Consumes Phase 3 RAG Pipeline without rebuilding retrieval.
    """

    NO_CONTEXT_MESSAGE = (
        "I couldn't find information about that in Akhil's portfolio. "
        "Feel free to drop Akhil a direct message via the contact form on the home page!"
    )

    def __init__(self, rag_pipeline: Any = None):
        self.rag_pipeline = rag_pipeline
        self.query_processor = QueryProcessor()
        self.context_builder = ContextBuilder()
        self.prompt_builder = SystemPromptBuilder()
        self.llm_client = LLMClient()
        self.validator = AnswerValidator()
        self.sse_formatter = SSEFormatter()

    def set_rag_pipeline(self, rag_pipeline: Any):
        """
        Sets or updates the underlying Phase 3 RAG pipeline instance.
        """
        self.rag_pipeline = rag_pipeline

    async def stream_chat(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        Executes end-to-end RAG chat pipeline, records stage latencies, and yields SSE stream strings.
        """
        t_start = time.perf_counter()
        retrieval_ms = 0.0
        llm_ms = 0.0

        try:
            # Step 1: Query Processing
            clean_query, inferred_filters = self.query_processor.process(
                request.query,
                history=request.history,
                user_filters=request.filters
            )

            # Step 2: Phase 3 Retrieval (Consumes retriever.search / pipeline.query)
            search_results = []
            t_retrieval_start = time.perf_counter()
            if self.rag_pipeline:
                try:
                    search_results = self.rag_pipeline.query(
                        query_text=clean_query,
                        mode="hybrid",
                        top_k=request.top_k or 5,
                        rerank=True,
                        metadata_filter=inferred_filters if inferred_filters else None
                    )
                except Exception as err:
                    print(f"[ChatbotService] Phase 3 Retrieval Warning: {err}")
            retrieval_ms = (time.perf_counter() - t_retrieval_start) * 1000

            # Early Exit: If no search results found, bypass LLM API immediately
            if not search_results:
                yield self.sse_formatter.format_sources(
                    sources=[],
                    related_projects=[],
                    conversation_id=request.conversation_id
                )
                words = self.NO_CONTEXT_MESSAGE.split(" ")
                for idx, word in enumerate(words):
                    token = word + (" " if idx < len(words) - 1 else "")
                    yield self.sse_formatter.format_token(token)
                yield self.sse_formatter.format_done(
                    confidence=0.0,
                    is_grounded=False,
                    conversation_id=request.conversation_id
                )

                total_ms = (time.perf_counter() - t_start) * 1000
                logger.info(
                    f"[Telemetry] req_id={request.conversation_id} "
                    f"retrieval={retrieval_ms:.1f}ms llm=0.0ms total={total_ms:.1f}ms "
                    f"results=0 grounded=False"
                )
                return

            # Step 3: Context, Citation & Related Project Building
            context_str, sources, related_projects = self.context_builder.build_context(search_results)

            # Emit sources event first (with related_projects & conversation_id)
            yield self.sse_formatter.format_sources(
                sources=sources,
                related_projects=related_projects,
                conversation_id=request.conversation_id
            )

            # Step 4: Prompt Construction
            prompt = self.prompt_builder.build_prompt(clean_query, context_str, request.history)

            # Step 5: LLM Token Streaming
            t_llm_start = time.perf_counter()
            full_response_acc = []
            async for token in self.llm_client.generate_stream(prompt, context_str):
                full_response_acc.append(token)
                yield self.sse_formatter.format_token(token)
            llm_ms = (time.perf_counter() - t_llm_start) * 1000

            # Step 6: Validation & Stream Completion
            full_answer = "".join(full_response_acc)
            is_grounded, confidence, _ = self.validator.validate(full_answer, sources)

            yield self.sse_formatter.format_done(
                confidence=confidence,
                is_grounded=is_grounded,
                conversation_id=request.conversation_id
            )

            total_ms = (time.perf_counter() - t_start) * 1000
            logger.info(
                f"[Telemetry] req_id={request.conversation_id} "
                f"retrieval={retrieval_ms:.1f}ms llm={llm_ms:.1f}ms total={total_ms:.1f}ms "
                f"results={len(search_results)} grounded={is_grounded}"
            )

        except Exception as e:
            print(f"[ChatbotService] Error during chat streaming: {e}")
            yield self.sse_formatter.format_error(str(e))

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Executes non-streaming chat query and returns complete ChatResponse object with telemetry.
        """
        t_start = time.perf_counter()

        clean_query, inferred_filters = self.query_processor.process(
            request.query,
            history=request.history,
            user_filters=request.filters
        )
        search_results = []
        t_retrieval_start = time.perf_counter()
        if self.rag_pipeline:
            try:
                search_results = self.rag_pipeline.query(
                    query_text=clean_query,
                    mode="hybrid",
                    top_k=request.top_k or 5,
                    rerank=True,
                    metadata_filter=inferred_filters if inferred_filters else None
                )
            except Exception as err:
                print(f"[ChatbotService] Phase 3 Retrieval Warning: {err}")
        retrieval_ms = (time.perf_counter() - t_retrieval_start) * 1000

        # Early Exit: If no search results found, return controlled refusal immediately
        if not search_results:
            total_ms = (time.perf_counter() - t_start) * 1000
            logger.info(
                f"[Telemetry] req_id={request.conversation_id} "
                f"retrieval={retrieval_ms:.1f}ms llm=0.0ms total={total_ms:.1f}ms "
                f"results=0 grounded=False"
            )
            return ChatResponse(
                answer=self.NO_CONTEXT_MESSAGE,
                sources=[],
                related_projects=[],
                conversation_id=request.conversation_id,
                confidence_score=0.0,
                is_grounded=False
            )

        context_str, sources, related_projects = self.context_builder.build_context(search_results)
        prompt = self.prompt_builder.build_prompt(clean_query, context_str, request.history)

        t_llm_start = time.perf_counter()
        full_response_acc = []
        async for token in self.llm_client.generate_stream(prompt, context_str):
            full_response_acc.append(token)
        llm_ms = (time.perf_counter() - t_llm_start) * 1000

        full_answer = "".join(full_response_acc)
        is_grounded, confidence, _ = self.validator.validate(full_answer, sources)

        total_ms = (time.perf_counter() - t_start) * 1000
        logger.info(
            f"[Telemetry] req_id={request.conversation_id} "
            f"retrieval={retrieval_ms:.1f}ms llm={llm_ms:.1f}ms total={total_ms:.1f}ms "
            f"results={len(search_results)} grounded={is_grounded}"
        )

        return ChatResponse(
            answer=full_answer,
            sources=sources,
            related_projects=related_projects,
            conversation_id=request.conversation_id,
            confidence_score=confidence,
            is_grounded=is_grounded
        )
