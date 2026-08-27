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
        "problem": "High quarterly subscriber churn of 12% causing revenue leakage across 25M+ customer accounts without early warning signals.",
        "solution": "Built an automated XGBoost predictive ML pipeline that flags high-risk churn signals 30 days prior to cancellation and triggers retention offers.",
        "my_contribution": "Architected the end-to-end ML pipeline, engineered 45+ domain features in Pandas/SQL, and integrated SHAP model interpretability.",
        "challenges": "Handling class imbalance (9:1 non-churn ratio) and optimizing inference latency under 25ms for 500k daily predictions.",
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
            "and persists them in ChromaDB."
        ),
        "problem": "Users spend hours manually searching long YouTube videos to find specific answers or technical explanations.",
        "solution": "Developed a full RAG pipeline with ChromaDB vector storage and Groq Llama 3.3 70B to instantly retrieve exact transcript context and generate grounded answers.",
        "my_contribution": "Built transcript ingestion, local SentenceTransformer 384D embedding generation, cosine similarity retrieval engine, FastAPI backend, and FastMCP agent tool integration.",
        "challenges": "Handling unsegmented multilingual transcripts and optimizing chunking parameters (800 char chunk / 150 char overlap) for semantic coherence.",
        "category": "Generative AI",
        "featured": True,
        "image": "project-yt-helper.png",
        "tags": [
            "Python", "FastAPI", "RAG", "LLMs", "Llama 3.3 70B", "Groq",
            "ChromaDB", "SentenceTransformers", "Embeddings", "Semantic Search", "MCP", "FastMCP"
        ],
        "demo_url": "",
        "repo_url": "https://github.com/sAkhil2027/yt_video-rag-chatbot",
        "metrics": [
            {"value": "384D", "label": "Embedding Dimensions"},
            {"value": "Top 7", "label": "Context Chunks"},
            {"value": "~5.6K", "label": "Retrieved Context"},
            {"value": "800 / 150", "label": "Chunk / Overlap"}
        ],
        "key_features": [
            "YouTube transcript ingestion pipeline using YouTubeTranscriptApi with support for manual and auto-generated transcript tracks.",
            "RAG pipeline using RecursiveCharacterTextSplitter with 800-character chunks and 150-character overlap.",
            "384-dimensional dense vector embeddings persisted in local ChromaDB collections.",
            "Semantic retrieval engine returning top 7 relevant transcript chunks for Llama 3.3 70B grounded generation.",
            "FastMCP server exposing ingest_youtube_video and query_youtube_video tools for AI agents (Cursor, Claude Desktop, Antigravity)."
        ],
        "architecture_highlights": (
            "Modular RAG architecture consisting of YouTube transcript extraction, SentenceTransformer embeddings, ChromaDB vector storage, cosine retrieval, and Groq Llama 3.3 70B generation."
        )
    },
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
        "problem": "Unpredictable multi-channel sales trends leading to stockouts and over-inventory costs.",
        "solution": "Implemented statistical time-series demand forecasting (Prophet & ARIMA) integrated with automated Power BI dashboards.",
        "my_contribution": "Designed PostgreSQL star-schema data warehouse, engineered seasonal trend decomposition algorithms, and authored executive BI reports.",
        "challenges": "Isolating holiday spikes and unexpected promotional variance from baseline organic demand trends.",
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
        "problem": "Slow manual quality control inspection causing production line bottlenecks and human audit errors.",
        "solution": "Trained real-time YOLOv8 deep learning vision models for automated surface defect detection at 35 FPS.",
        "my_contribution": "Collected & annotated custom industrial image dataset, performed albumentations data pipeline augmentation, and trained YOLOv8 model.",
        "challenges": "Maintaining high mAP precision under reflective factory lighting conditions and executing 35 FPS inference on edge hardware.",
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
