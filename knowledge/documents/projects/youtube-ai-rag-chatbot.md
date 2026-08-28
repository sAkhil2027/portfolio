# YT Helper — YouTube AI RAG Chatbot & API

## Overview
A Retrieval-Augmented Generation (RAG) system that extracts YouTube video transcripts, converts them into vector embeddings, retrieves relevant context, and generates grounded answers using Groq-powered Llama 3.3 70B.

## Problem
Users spend hours manually searching long YouTube videos to find specific answers or technical explanations.

## Solution
Developed a full RAG pipeline with ChromaDB vector storage and Groq Llama 3.3 70B to instantly retrieve exact transcript context and generate grounded answers.

## Architecture
Modular RAG architecture consisting of YouTube transcript extraction (YouTubeTranscriptApi), RecursiveCharacterTextSplitter chunking, SentenceTransformer dense embeddings (384D), ChromaDB vector storage, cosine similarity retrieval engine, FastAPI REST API, and FastMCP agent tool integration.

## Technologies
- Python
- FastAPI
- RAG
- LLMs
- Llama 3.3 70B
- Groq
- ChromaDB
- SentenceTransformers
- Embeddings
- Semantic Search
- FastMCP

## Features
- YouTube transcript ingestion pipeline using YouTubeTranscriptApi with support for manual and auto-generated transcript tracks.
- RAG pipeline using RecursiveCharacterTextSplitter with 800-character chunks and 150-character overlap.
- 384-dimensional dense vector embeddings persisted in local ChromaDB collections.
- Semantic retrieval engine returning top 7 relevant transcript chunks for Llama 3.3 70B grounded generation.
- FastMCP server exposing ingest_youtube_video and query_youtube_video tools for AI agents (Cursor, Claude Desktop, Antigravity).

## My Contribution
Built transcript ingestion, local SentenceTransformer 384D embedding generation, cosine similarity retrieval engine, FastAPI backend, and FastMCP agent tool integration.

## Challenges
- Handling unsegmented multilingual transcripts.
- Optimizing chunking parameters (800 char chunk / 150 char overlap) for semantic coherence.

## Results
- 384D Embedding Dimensions
- Top 7 Context Chunks
- ~5.6K Retrieved Context
- 800 / 150 Chunk / Overlap

## Links
- **GitHub**: https://github.com/sAkhil2027/yt_video-rag-chatbot
- **Demo**: N/A
