"""
Projects data module for Akhil - Data Science, Data Analytics & AI/ML Projects.
Standardized for Pydantic Project Schema and RAG Document Ingestion.
"""

PROJECTS = [
    {
        "id": "1",
        "slug": "customer-churn-prediction-ml",
        "name": "Customer Churn Prediction & Lifetime Value ML Engine",
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
        "role": "Architected the end-to-end ML pipeline, engineered 45+ domain features in Pandas/SQL, and integrated SHAP model interpretability.",
        "my_contribution": "Architected the end-to-end ML pipeline, engineered 45+ domain features in Pandas/SQL, and integrated SHAP model interpretability.",
        "challenges": ["Handling class imbalance (9:1 non-churn ratio)", "Optimizing inference latency under 25ms for 500k daily predictions."],
        "category": "Machine Learning",
        "featured": True,
        "image": "project-cloud-analytics.png",
        "technologies": ["Python", "Scikit-Learn", "XGBoost", "Pandas", "FastAPI", "Streamlit"],
        "tags": ["Python", "Scikit-Learn", "XGBoost", "Pandas", "FastAPI", "Streamlit"],
        "demo": "https://churn-ml-demo.akhil.dev",
        "demo_url": "https://churn-ml-demo.akhil.dev",
        "github": "https://github.com/akhil-data/customer-churn-ml",
        "repo_url": "https://github.com/akhil-data/customer-churn-ml",
        "results": [
            "94.2% AUC-ROC Score",
            "25M+ Records Analyzed",
            "18% Churn Reduced",
            "< 25ms Inference Speed"
        ],
        "metrics": [
            {"value": "94.2%", "label": "AUC-ROC Score"},
            {"value": "25M+", "label": "Records Analyzed"},
            {"value": "18%", "label": "Churn Reduced"},
            {"value": "< 25ms", "label": "Inference Speed"}
        ],
        "features": [
            "Comprehensive Exploratory Data Analysis (EDA) uncovering key behavioral churn triggers.",
            "Feature engineering pipeline creating 45+ domain-specific metrics (recency, frequency, monetary value).",
            "SHAP (SHapley Additive exPlanations) model interpretability dashboard for executive decision making.",
            "Automated Streamlit interactive web application for marketing teams to run instant predictions."
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
        "id": "2",
        "slug": "youtube-ai-rag-chatbot",
        "name": "YT Helper — YouTube AI RAG Chatbot & API",
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
        "role": "Built transcript ingestion, local SentenceTransformer 384D embedding generation, cosine similarity retrieval engine, FastAPI backend, and FastMCP agent tool integration.",
        "my_contribution": "Built transcript ingestion, local SentenceTransformer 384D embedding generation, cosine similarity retrieval engine, FastAPI backend, and FastMCP agent tool integration.",
        "challenges": ["Handling unsegmented multilingual transcripts", "Optimizing chunking parameters (800 char chunk / 150 char overlap) for semantic coherence."],
        "category": "Generative AI",
        "featured": True,
        "image": "project-yt-helper.png",
        "technologies": [
            "Python", "FastAPI", "RAG", "LLMs", "Llama 3.3 70B", "Groq",
            "ChromaDB", "SentenceTransformers", "Embeddings", "Semantic Search", "MCP", "FastMCP"
        ],
        "tags": [
            "Python", "FastAPI", "RAG", "LLMs", "Llama 3.3 70B", "Groq",
            "ChromaDB", "SentenceTransformers", "Embeddings", "Semantic Search", "MCP", "FastMCP"
        ],
        "demo": "",
        "demo_url": "",
        "github": "https://github.com/sAkhil2027/yt_video-rag-chatbot",
        "repo_url": "https://github.com/sAkhil2027/yt_video-rag-chatbot",
        "results": [
            "384D Embedding Dimensions",
            "Top 7 Context Chunks",
            "~5.6K Retrieved Context",
            "800 / 150 Chunk / Overlap"
        ],
        "metrics": [
            {"value": "384D", "label": "Embedding Dimensions"},
            {"value": "Top 7", "label": "Context Chunks"},
            {"value": "~5.6K", "label": "Retrieved Context"},
            {"value": "800 / 150", "label": "Chunk / Overlap"}
        ],
        "features": [
            "YouTube transcript ingestion pipeline using YouTubeTranscriptApi with support for manual and auto-generated transcript tracks.",
            "RAG pipeline using RecursiveCharacterTextSplitter with 800-character chunks and 150-character overlap.",
            "384-dimensional dense vector embeddings persisted in local ChromaDB collections.",
            "Semantic retrieval engine returning top 7 relevant transcript chunks for Llama 3.3 70B grounded generation.",
            "FastMCP server exposing ingest_youtube_video and query_youtube_video tools for AI agents (Cursor, Claude Desktop, Antigravity)."
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
        "id": "3",
        "slug": "laptop-price-prediction",
        "name": "Laptop Price Prediction — Machine Learning",
        "title": "Laptop Price Prediction — Machine Learning",
        "tagline": "ML-powered laptop price prediction using feature engineering and Random Forest regression.",
        "description": (
            "An end-to-end Machine Learning system that predicts laptop prices from hardware and "
            "specifications using data preprocessing, feature engineering, Scikit-learn pipelines, "
            "and a Random Forest Regressor."
        ),
        "long_description": (
            "Laptop Price Prediction is an end-to-end Machine Learning project that estimates laptop "
            "prices based on specifications such as RAM, processor, GPU, storage, display, operating "
            "system, and laptop type. The system performs data cleaning, feature engineering, exploratory "
            "data analysis, categorical encoding, model training, and evaluation using a Scikit-learn "
            "pipeline. A Random Forest Regressor is trained on the processed features and serialized "
            "using Pickle for future deployment in applications such as Streamlit or Flask."
        ),
        "problem": "Laptop prices vary significantly based on hardware specifications, making it difficult to estimate a fair market price manually.",
        "solution": "Developed a machine learning regression pipeline that preprocesses laptop specifications, engineers meaningful hardware features, and predicts laptop prices using Random Forest regression.",
        "role": "Built the complete ML workflow including data preprocessing, feature engineering, EDA, categorical transformation, Scikit-learn pipeline construction, Random Forest training, model evaluation, and model serialization.",
        "my_contribution": "Built the complete ML workflow including data preprocessing, feature engineering, EDA, categorical transformation, Scikit-learn pipeline construction, Random Forest training, model evaluation, and model serialization.",
        "challenges": ["Handling inconsistent laptop specification formats such as RAM, weight, CPU, GPU, storage, and screen resolution."],
        "category": "Machine Learning",
        "featured": False,
        "image": "project-laptop-price.png",
        "technologies": [
            "Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning",
            "Random Forest", "Regression", "Feature Engineering", "EDA", "Data Preprocessing"
        ],
        "tags": [
            "Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning",
            "Random Forest", "Regression", "Feature Engineering", "EDA", "Data Preprocessing"
        ],
        "demo": "",
        "demo_url": "",
        "github": "https://github.com/sAkhil2027/Laptop-Price-Prediction",
        "repo_url": "https://github.com/sAkhil2027/Laptop-Price-Prediction",
        "results": [
            "100 Random Forest Estimators",
            "15 Maximum Tree Depth",
            "0.75 Feature Sampling",
            "High R² + Low MAE Evaluation Metrics"
        ],
        "metrics": [
            {"value": "100", "label": "Random Forest Estimators"},
            {"value": "15", "label": "Maximum Tree Depth"},
            {"value": "0.75", "label": "Feature Sampling"},
            {"value": "R² + MAE", "label": "Evaluation Metrics"}
        ],
        "features": [
            "Complete data preprocessing pipeline for cleaning and transforming raw laptop specifications.",  
            "Feature engineering for display resolution, PPI, CPU categories, storage capacities, GPU brands, and operating systems.",
            "Exploratory Data Analysis covering company, laptop type, RAM, CPU, GPU, operating system, touchscreen, IPS display, and price relationships.",
            "Scikit-learn machine learning pipeline combining categorical feature transformation with a Random Forest Regressor.",
            "Serialized trained pipeline using Pickle, making the model ready for integration with Streamlit, Flask, or FastAPI applications."
        ],
        "key_features": [
            "Complete data preprocessing pipeline for cleaning and transforming raw laptop specifications.",  
            "Feature engineering for display resolution, PPI, CPU categories, storage capacities, GPU brands, and operating systems.",
            "Exploratory Data Analysis covering company, laptop type, RAM, CPU, GPU, operating system, touchscreen, IPS display, and price relationships.",
            "Scikit-learn machine learning pipeline combining categorical feature transformation with a Random Forest Regressor.",
            "Serialized trained pipeline using Pickle, making the model ready for integration with Streamlit, Flask, or FastAPI applications."
        ],
        "architecture_highlights": (
            "End-to-end machine learning architecture consisting of laptop specification preprocessing, "
            "feature engineering, exploratory analysis, categorical encoding through ColumnTransformer, "
            "Random Forest regression, model evaluation using R² and MAE, and Pickle-based model serialization."
        )
    },
    {
        "id": "4",
        "slug": "multi-utility-rag-chatbot",
        "name": "Multi Utility RAG Chatbot — LangGraph & FAISS",
        "title": "Multi Utility RAG Chatbot — LangGraph & FAISS",
        "tagline": "Stateful multi-tool RAG chatbot with document retrieval, web search, calculator tools, and persistent conversations.",
        "description": (
            "An advanced Retrieval-Augmented Generation (RAG) chatbot built with LangGraph, LangChain, "
            "FAISS, OpenRouter, and Streamlit that enables users to interact with uploaded PDFs while "
            "also using intelligent tools such as web search and calculation."
        ),
        "long_description": (
            "Multi Utility RAG Chatbot is an end-to-end conversational AI system that combines document "
            "retrieval, tool calling, stateful workflows, and persistent memory. Users can upload PDFs, "
            "which are parsed using PyPDFLoader, split into overlapping chunks, converted into embeddings "
            "using the all-MiniLM-L6-v2 SentenceTransformer model, and stored in a FAISS vector database."
        ),
        "problem": "Users need a single conversational interface that can answer questions from their documents while also handling general queries requiring web search or calculations.",
        "solution": "Built a stateful LangGraph-based AI agent that combines PDF RAG, semantic retrieval, web search, calculator tools, persistent conversation memory, and streaming LLM responses.",
        "role": "Built the RAG pipeline, PDF ingestion and chunking workflow, HuggingFace embedding generation, FAISS retrieval, LangGraph agent workflow, tool integrations, SQLite conversation checkpointing, and Streamlit chat interface.",
        "my_contribution": "Built the RAG pipeline, PDF ingestion and chunking workflow, HuggingFace embedding generation, FAISS retrieval, LangGraph agent workflow, tool integrations, SQLite conversation checkpointing, and Streamlit chat interface.",
        "challenges": ["Designing a stateful workflow combining document retrieval with external tools", "Maintaining conversation history across multiple chat threads in real time."],
        "category": "Generative AI",
        "featured": False,
        "image": "project-multi-utility-rag.png",
        "technologies": [
            "Python", "Streamlit", "LangGraph", "LangChain", "RAG", "LLMs",
            "OpenRouter", "GPT-4o-mini", "FAISS", "HuggingFace", "Embeddings", "SQLite"
        ],
        "tags": [
            "Python", "Streamlit", "LangGraph", "LangChain", "RAG", "LLMs",
            "OpenRouter", "GPT-4o-mini", "FAISS", "HuggingFace", "Embeddings", "SQLite"
        ],
        "demo": "",
        "demo_url": "",
        "github": "https://github.com/sAkhil2027/panscience-Multi-Utility-RAG-Chatbot-",
        "repo_url": "https://github.com/sAkhil2027/panscience-Multi-Utility-RAG-Chatbot-",
        "results": [
            "1000 / 200 Chunk / Overlap",
            "3 Integrated AI Tools",
            "SQLite Persistent Memory",
            "Real-time Response Streaming"
        ],
        "metrics": [
            {"value": "1000 / 200", "label": "Chunk / Overlap"},
            {"value": "3", "label": "Integrated AI Tools"},
            {"value": "SQLite", "label": "Persistent Memory"},
            {"value": "Real-time", "label": "Response Streaming"}
        ],
        "features": [
            "Dynamic PDF upload and document ingestion using PyPDFLoader with recursive text chunking.",
            "Semantic RAG pipeline using HuggingFace all-MiniLM-L6-v2 embeddings and FAISS vector similarity search.",
            "Multi-tool AI agent integrating PDF retrieval, DuckDuckGo web search, and calculator functionality through LangGraph workflows.",
            "Persistent multi-thread conversation memory using SQLite checkpointing with support for restoring previous conversations."
        ],
        "key_features": [
            "Dynamic PDF upload and document ingestion using PyPDFLoader with recursive text chunking.",
            "Semantic RAG pipeline using HuggingFace all-MiniLM-L6-v2 embeddings and FAISS vector similarity search.",
            "Multi-tool AI agent integrating PDF retrieval, DuckDuckGo web search, and calculator functionality through LangGraph workflows.",
            "Persistent multi-thread conversation memory using SQLite checkpointing with support for restoring previous conversations."
        ],
        "architecture_highlights": (
            "Stateful agentic RAG architecture consisting of PDF ingestion, PyPDFLoader parsing, recursive "
            "text chunking, HuggingFace embeddings, FAISS vector storage, similarity retrieval, LangGraph "
            "workflow orchestration, multi-tool execution, OpenRouter GPT-4o-mini generation, SQLite-based "
            "checkpointing, and Streamlit response streaming."
        )
    },
    {
        "id": "5",
        "slug": "diwali-sales-analysis",
        "name": "Diwali Sales Analysis — EDA & Business Insights",
        "title": "Diwali Sales Analysis — EDA & Business Insights",
        "tagline": "Exploratory data analysis of Diwali sales to uncover customer, geographic, occupational, and product-level purchasing patterns.",
        "description": (
            "An end-to-end Exploratory Data Analysis (EDA) project that analyzes Diwali sales data "
            "using Python, Pandas, Matplotlib, and Seaborn to identify customer demographics, "
            "purchasing behavior, geographic trends, occupation patterns, and product performance."
        ),
        "long_description": (
            "Diwali Sales Analysis is an exploratory data analysis project performed on a dataset "
            "containing 11,251 records and 15 columns representing customer demographics, geographic "
            "information, occupations, products, orders, and purchase amounts."
        ),
        "problem": "Raw sales data contains multiple customer, geographic, demographic, and product dimensions, making it difficult to identify meaningful purchasing patterns directly.",
        "solution": "Built a complete EDA workflow that cleans the sales dataset and analyzes customer demographics, geographic performance, occupations, product categories, and order behavior.",
        "role": "Performed the complete data analysis workflow including dataset inspection, data cleaning, missing-value handling, data type conversion, descriptive statistics, Pandas aggregations, and business-oriented visualizations.",
        "my_contribution": "Performed the complete data analysis workflow including dataset inspection, data cleaning, missing-value handling, data type conversion, descriptive statistics, Pandas aggregations, and business-oriented visualizations.",
        "challenges": ["Cleaning an initially inconsistent sales dataset while identifying the most meaningful dimensions for analysis."],
        "category": "Data Analysis",
        "featured": False,
        "image": "project-diwali-sales.png",
        "technologies": [
            "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "EDA",
            "Data Analysis", "Data Cleaning", "Data Visualization", "Business Analytics"
        ],
        "tags": [
            "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "EDA",
            "Data Analysis", "Data Cleaning", "Data Visualization", "Business Analytics"
        ],
        "demo": "",
        "demo_url": "",
        "github": "https://github.com/sAkhil2027/diwali-sale-anaysis",
        "repo_url": "https://github.com/sAkhil2027/diwali-sale-anaysis",
        "results": [
            "11.2K+ Initial Records",
            "11,239 Clean Records",
            "13 Analyzed Columns",
            "7+ Analytical Dimensions"
        ],
        "metrics": [
            {"value": "11.2K+", "label": "Initial Records"},
            {"value": "11,239", "label": "Clean Records"},
            {"value": "13", "label": "Analyzed Columns"},
            {"value": "7+", "label": "Analytical Dimensions"}
        ],
        "features": [
            "End-to-end data cleaning workflow that removes irrelevant columns, handles missing Amount records, and converts fields.",
            "Customer demographic analysis covering gender, age groups, and marital status.",
            "Geographic analysis comparing states using both total order volume and total sales amount.",
            "Occupation-level analysis using customer/order distribution and aggregated sales amount."
        ],
        "key_features": [
            "End-to-end data cleaning workflow that removes irrelevant columns, handles missing Amount records, and converts fields.",
            "Customer demographic analysis covering gender, age groups, and marital status.",
            "Geographic analysis comparing states using both total order volume and total sales amount.",
            "Occupation-level analysis using customer/order distribution and aggregated sales amount."
        ],
        "architecture_highlights": (
            "End-to-end exploratory data analysis architecture consisting of CSV data ingestion, "
            "initial dataset inspection, removal of irrelevant columns, missing-value handling, "
            "data type conversion, descriptive statistics, Pandas-based aggregation, and "
            "multi-dimensional visualization."
        )
    },
    {
        "id": "6",
        "slug": "iphone-ecommerce-sales-analysis",
        "name": "iPhone E-Commerce Sales Analysis — EDA & Business Insights",
        "title": "iPhone E-Commerce Sales Analysis — EDA & Business Insights",
        "tagline": "Business-focused EDA of iPhone e-commerce data across products, platforms, pricing, geography, and seasonality.",
        "description": (
            "An end-to-end Exploratory Data Analysis (EDA) project on Indian iPhone "
            "e-commerce data using Python, Pandas, Matplotlib, and Seaborn to uncover "
            "product demand, pricing patterns, platform behavior, geographic trends, "
            "and purchasing patterns."
        ),
        "long_description": (
            "iPhone E-Commerce Sales Analysis is an end-to-end data analysis project "
            "performed on 5,843 records containing product, pricing, platform, geographic, "
            "and temporal information."
        ),
        "problem": "E-commerce product data contains multiple dimensions such as model, storage, color, platform, location, date, and price, making it difficult to identify meaningful demand patterns.",
        "solution": "Built a comprehensive EDA pipeline that cleans and transforms raw iPhone e-commerce data into structured product, geographic, platform, and temporal features.",
        "role": "Performed data cleaning, date feature engineering, product attribute extraction, platform comparison, geographic analysis, seasonality analysis, and pricing analysis.",
        "my_contribution": "Performed data cleaning, date feature engineering, product attribute extraction, platform comparison, geographic analysis, seasonality analysis, and pricing analysis.",
        "challenges": ["Handling inconsistent product names while extracting model, generation, storage, and color attributes."],
        "category": "Data Analysis",
        "featured": False,
        "image": "project-iphone-analysis.png",
        "technologies": [
            "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "EDA",
            "Data Analysis", "Feature Engineering", "Pricing Analysis", "E-Commerce Analytics"
        ],
        "tags": [
            "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "EDA",
            "Data Analysis", "Feature Engineering", "Pricing Analysis", "E-Commerce Analytics"
        ],
        "demo": "",
        "demo_url": "",
        "github": "https://github.com/sAkhil2027/iphone_dataset_analysis",
        "repo_url": "https://github.com/sAkhil2027/iphone_dataset_analysis",
        "results": [
            "5,843 Dataset Records",
            "151 Unique Products",
            "3 E-Commerce Platforms",
            "347 Unique Dates"
        ],
        "metrics": [
            {"value": "5,843", "label": "Dataset Records"},
            {"value": "151", "label": "Unique Products"},
            {"value": "3", "label": "E-Commerce Platforms"},
            {"value": "347", "label": "Unique Dates"}
        ],
        "features": [
            "Comprehensive data-quality analysis identifying empty, low-variation, redundant, and identifier columns.",
            "Temporal feature engineering from transaction dates including year, month, day name, and weekend flags.",
            "Product feature extraction using regular expressions to derive iPhone model, generation, storage capacity, and color.",
            "Platform-level pricing analysis comparing Amazon, Flipkart, and JioMart."
        ],
        "key_features": [
            "Comprehensive data-quality analysis identifying empty, low-variation, redundant, and identifier columns.",
            "Temporal feature engineering from transaction dates including year, month, day name, and weekend flags.",
            "Product feature extraction using regular expressions to derive iPhone model, generation, storage capacity, and color.",
            "Platform-level pricing analysis comparing Amazon, Flipkart, and JioMart."
        ],
        "architecture_highlights": (
            "End-to-end exploratory analytics architecture consisting of raw e-commerce data "
            "ingestion, data-quality inspection, regex-based product feature extraction, Pandas "
            "aggregation, and Matplotlib/Seaborn visualization."
        )
    }
]