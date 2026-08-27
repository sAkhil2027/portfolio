"""
Projects data module for Akhil - Data Science, Data Analytics & AI/ML Projects.
"""

PROJECTS = [
    {
        "id": 1,
        "slug": "customer-churn-prediction-ml",
        "title": "Customer Churn Prediction & Lifetime Value ML Engine",
        "tagline": "End-to-end predictive machine learning pipeline for subscriber churn and CLV forecasting.",
        "description": "An end-to-end Machine Learning pipeline analyzing 25M+ customer transaction rows to predict subscription churn risk and calculate Customer Lifetime Value (CLV).",
        "long_description": (
            "This machine learning system combines feature engineering, automated EDA, hyperparameter tuning, and ensemble modeling. "
            "Engineered with Python, XGBoost, Scikit-Learn, and FastAPI, the model identifies high-risk churn signals 30 days before user cancellation "
            "and recommends personalized retention offers with an 18% improvement in customer retention."
        ),
        "category": "Machine Learning",
        "featured": True,
        "image": "project-cloud-analytics.png",
        "tags": ["Python", "Scikit-Learn", "XGBoost", "Pandas", "FastAPI", "Streamlit"],
        "demo_url": "https://churn-ml-demo.akhil.dev",
        "repo_url": "https://github.com/akhil-data/customer-churn-ml",
        "metrics": [
            {"value": "94.2%", "label": "AUC-ROC Score"},
            {"value": "25M+", "label": "Records Analyzed"},
            {"value": "18%", "label": "Churn Reduced"},
            {"value": "< 25ms", "label": "Inference Speed"}
        ],
        "key_features": [
            "Comprehensive Exploratory Data Analysis (EDA) uncovering key behavioral churn triggers.",
            "Feature engineering pipeline creating 45+ domain-specific metrics (recency, frequency, monetary value).",
            "SHAP (SHapley Additive exPlanations) model interpretability dashboard for executive decision making.",
            "Automated Streamlit interactive web application for marketing teams to run instant predictions."
        ],
        "architecture_highlights": (
            "Employs Optuna for automated hyperparameter tuning and MLflow for experiment tracking, model lineage, and artifact logging."
        )
    },
     {
    "id": 2,
    "slug": "youtube-ai-rag-chatbot",
    "title": "YT Helper — YouTube AI RAG Chatbot & API",
    "tagline": "Chat with any YouTube video using RAG, semantic search, and Llama 3.3 70B.",
    "description": (
        "A Retrieval-Augmented Generation (RAG) system that extracts YouTube video transcripts, "
        "converts them into vector embeddings, retrieves relevant context, and generates grounded "
        "answers using Groq-powered Llama 3.3 70B."
    ),
    "long_description": (
        "YT Helper is an end-to-end Retrieval-Augmented Generation (RAG) application that enables "
        "users to ask questions about YouTube videos without watching the entire video. The system "
        "extracts available transcript content using YouTubeTranscriptApi, splits it into semantic "
        "chunks, generates 384-dimensional dense embeddings locally with SentenceTransformers, "
        "and persists them in ChromaDB. For every user query, cosine similarity search retrieves "
        "the top 7 most relevant transcript chunks and supplies the retrieved context to "
        "Groq Cloud's Llama 3.3 70B model for grounded response generation. The application also "
        "provides FastAPI REST endpoints, an interactive dark-mode chatbot interface, and a "
        "FastMCP server that exposes the RAG pipeline as tools for external AI agents."
    ),

    "category": "Generative AI",
    "featured": True,

    "image": "project-yt-helper.png",

    "tags": [
        "Python",
        "FastAPI",
        "RAG",
        "LLMs",
        "Llama 3.3 70B",
        "Groq",
        "ChromaDB",
        "SentenceTransformers",
        "Embeddings",
        "Semantic Search",
        "MCP",
        "FastMCP"
    ],

    "demo_url": "",
    "repo_url": "https://github.com/sAkhil2027/yt_video-rag-chatbot",

    "metrics": [
        {
            "value": "384D",
            "label": "Embedding Dimensions"
        },
        {
            "value": "Top 7",
            "label": "Context Chunks"
        },
        {
            "value": "~5.6K",
            "label": "Retrieved Context"
        },
        {
            "value": "800 / 150",
            "label": "Chunk / Overlap"
        }
    ],

    "key_features": [
        (
            "Built a complete YouTube transcript ingestion pipeline using YouTubeTranscriptApi "
            "with support for manual and auto-generated multilingual transcript tracks."
        ),
        (
            "Implemented a RAG pipeline using RecursiveCharacterTextSplitter with 800-character "
            "chunks and 150-character overlap to preserve contextual continuity across transcript segments."
        ),
        (
            "Generated 384-dimensional dense vector embeddings locally using "
            "SentenceTransformers all-MiniLM-L6-v2 and persisted them in ChromaDB collections."
        ),
        (
            "Developed a semantic retrieval engine using cosine similarity search to retrieve "
            "the top 7 relevant transcript chunks, providing approximately 5,600 characters "
            "of contextual information to the LLM."
        ),
        (
            "Integrated Groq Cloud's Llama 3.3 70B model for high-speed, context-grounded "
            "question answering over retrieved YouTube transcript content."
        ),
        (
            "Developed FastAPI REST endpoints for video ingestion and question answering, "
            "along with an interactive dark-mode chatbot frontend."
        ),
        (
            "Implemented a FastMCP server exposing ingest_youtube_video and query_youtube_video "
            "tools for integration with external AI agents such as Claude Desktop, Cursor, and Antigravity."
        )
    ],

    "architecture_highlights": (
        "Uses a modular RAG architecture consisting of YouTube transcript extraction, semantic "
        "text chunking, SentenceTransformer embeddings, persistent ChromaDB vector storage, "
        "cosine similarity retrieval, and Groq Llama 3.3 70B generation. The backend is exposed "
        "through FastAPI REST endpoints while FastMCP provides a separate agent integration layer. "
        "Core functionality is separated into transcript extraction, embedding/vector storage, "
        "retrieval, and LLM service modules for maintainability."
    )
},
    # {
    #     "id": 2,
    #     "slug": "generative-ai-rag-search",
    #     "title": "Enterprise Generative AI & RAG Search System",
    #     "tagline": "LLM-powered document intelligence and semantic search engine using LangChain and Vector DBs.",
    #     "description": "A Retrieval-Augmented Generation (RAG) AI application that indexes complex PDF/text documentation and answers domain-specific natural language queries.",
    #     "long_description": (
    #         "Built with PyTorch, LangChain, FAISS Vector Index, and Llama 3 / OpenAI models. "
    #         "This AI system enables users to ask complex questions across thousands of technical and financial documents, "
    #         "delivering accurate context-aware responses with exact page-level source citations and zero hallucination."
    #     ),
    #     "category": "AI & NLP",
    #     "featured": True,
    #     "image": "project-ai-copilot.png",
    #     "tags": ["Python", "PyTorch", "LangChain", "FAISS", "Llama 3", "OpenAI API"],
    #     "demo_url": "https://rag-ai-demo.akhil.dev",
    #     "repo_url": "https://github.com/akhil-data/generative-ai-rag-search",
    #     "metrics": [
    #         {"value": "96.4%", "label": "Retrieval Precision"},
    #         {"value": "10k+", "label": "Docs Indexed"},
    #         {"value": "< 280ms", "label": "Vector Search Latency"},
    #         {"value": "4.2x", "label": "Research Speedup"}
    #     ],
    #     "key_features": [
    #         "Semantic chunking and vector embedding pipeline using HuggingFace sentence-transformers.",
    #         "Hybrid search combining BM25 keyword matching with Dense Vector embeddings for maximum recall.",
    #         "Interactive Streamlit & FastAPI web interface with streaming token response rendering.",
    #         "Custom guardrails filtering prompt injection and out-of-scope enterprise queries."
    #     ],
    #     "architecture_highlights": (
    #         "Vector embeddings are stored in FAISS / Pinecone DB with HNSW index topology for sub-linear similarity search across millions of embedding vectors."
    #     )
    # },
    {
        "id": 3,
        "slug": "bi-dashboard-sales-forecasting",
        "title": "Executive BI Analytics & Sales Forecasting Engine",
        "tagline": "Interactive business intelligence suite with time-series demand forecasting models.",
        "description": "An interactive Power BI and Plotly Dash analytics suite powered by Meta's Prophet for automated revenue, inventory, and demand forecasting.",
        "long_description": (
            "Designed for executive leadership, this platform aggregates multi-channel sales data into real-time BI dashboards. "
            "Utilizes statistical time-series models (Prophet & ARIMA) to project quarterly revenue trends, seasonal spikes, and optimal stock levels."
        ),
        "category": "Data Analytics & BI",
        "featured": True,
        "image": "project-task-orchestrator.png",
        "tags": ["Python", "SQL", "Power BI", "Prophet", "Plotly", "PostgreSQL"],
        "demo_url": "https://bi-analytics-demo.akhil.dev",
        "repo_url": "https://github.com/akhil-data/bi-sales-forecasting",
        "metrics": [
            {"value": "98.1%", "label": "Forecast Accuracy"},
            {"value": "50+", "label": "KPIs Monitored"},
            {"value": "< 1s", "label": "Dashboard Refresh"},
            {"value": "$120k", "label": "Inventory Savings"}
        ],
        "key_features": [
            "Automated SQL ETL pipelines ingesting daily sales feeds into data warehouse schemas.",
            "Decomposed time-series models isolating baseline trend, weekly seasonality, and holiday effects.",
            "Interactive Power BI and Plotly Dash visuals with drill-down capabilities by region and product line.",
            "Automated anomaly detection triggering email alerts on unexpected sales drops."
        ],
        "architecture_highlights": (
            "Built with star-schema relational data model in PostgreSQL optimized with indexes and materialized views for sub-second analytical queries."
        )
    },
    {
        "id": 4,
        "slug": "computer-vision-defect-detection",
        "title": "Computer Vision Defect Inspection System",
        "tagline": "Real-time automated visual quality control powered by YOLOv8 deep neural networks.",
        "description": "A deep learning computer vision model detecting manufacturing anomalies and surface flaws in real-time camera video streams.",
        "long_description": (
            "Trained on custom industrial image datasets using YOLOv8 and PyTorch. "
            "The system processes video feeds at 35 FPS, identifying micro-scratches, dents, and assembly defects with high precision."
        ),
        "category": "Computer Vision",
        "featured": False,
        "image": "project-ecommerce.png",
        "tags": ["PyTorch", "YOLOv8", "OpenCV", "Python", "Flask", "Docker"],
        "demo_url": "https://cv-defect-demo.akhil.dev",
        "repo_url": "https://github.com/akhil-data/cv-defect-detection",
        "metrics": [
            {"value": "99.1%", "label": "mAP@0.5 Score"},
            {"value": "35 FPS", "label": "Real-Time Speed"},
            {"value": "95%", "label": "Manual Audit Saved"}
        ],
        "key_features": [
            "Real-time object detection and instance segmentation for assembly line cameras.",
            "Data augmentation pipeline expanding dataset variance for lighting and reflection robustness.",
            "Web dashboard visualizing defect confidence scores and historical flaw counts."
        ],
        "architecture_highlights": (
            "Optimized deep learning inference with TensorRT GPU acceleration."
        )
    }
]
