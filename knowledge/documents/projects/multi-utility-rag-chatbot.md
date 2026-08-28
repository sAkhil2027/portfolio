# Multi Utility RAG Chatbot — LangGraph & FAISS

## Overview
An advanced Retrieval-Augmented Generation (RAG) chatbot built with LangGraph, LangChain, FAISS, OpenRouter, and Streamlit that enables users to interact with uploaded PDFs while also using intelligent tools such as web search and calculation.

## Problem
Users need a single conversational interface that can answer questions from their documents while also handling general queries requiring web search or calculations.

## Solution
Built a stateful LangGraph-based AI agent that combines PDF RAG, semantic retrieval, web search, calculator tools, persistent conversation memory, and streaming LLM responses.

## Architecture
Stateful agentic RAG architecture consisting of PDF ingestion, PyPDFLoader parsing, recursive text chunking, HuggingFace embeddings, FAISS vector storage, similarity retrieval, LangGraph workflow orchestration, multi-tool execution, OpenRouter GPT-4o-mini generation, SQLite-based checkpointing, and Streamlit response streaming.

## Technologies
- Python
- Streamlit
- LangGraph
- LangChain
- RAG
- LLMs
- OpenRouter
- GPT-4o-mini
- FAISS
- HuggingFace
- Embeddings
- SQLite

## Features
- Dynamic PDF upload and document ingestion using PyPDFLoader with recursive text chunking.
- Semantic RAG pipeline using HuggingFace all-MiniLM-L6-v2 embeddings and FAISS vector similarity search.
- Multi-tool AI agent integrating PDF retrieval, DuckDuckGo web search, and calculator functionality through LangGraph workflows.
- Persistent multi-thread conversation memory using SQLite checkpointing with support for restoring previous conversations.
- Real-time LLM response streaming through Streamlit for a ChatGPT-like conversational experience.

## My Contribution
Built the RAG pipeline, PDF ingestion and chunking workflow, HuggingFace embedding generation, FAISS retrieval, LangGraph agent workflow, tool integrations, SQLite conversation checkpointing, and Streamlit chat interface.

## Challenges
- Designing a stateful workflow combining document retrieval with external tools.
- Maintaining conversation history across multiple chat threads in real time.

## Results
- 1000 / 200 Chunk / Overlap
- 3 Integrated AI Tools
- SQLite Persistent Memory
- Real-time Response Streaming

## Links
- **GitHub**: https://github.com/sAkhil2027/panscience-Multi-Utility-RAG-Chatbot-
- **Demo**: N/A
