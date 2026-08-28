"""
Experience data module for Akhil - Data Science, AI/ML Roles, Hackathons & Competitions.
Standardized for Pydantic Experience Schema and RAG Document Ingestion.
"""

EXPERIENCE = [
    {
        "company": "Cognitive AI Labs",
        "role": "AI/ML Engineer & RAG System Developer",
        "type": "Full-Time",
        "start_date": "2026",
        "end_date": "Present",
        "year": "2026",
        "period": "2026 - Present",
        "location": "Remote / India",
        "description": "Leading RAG pipeline development, agentic workflows with Model Context Protocol (MCP), and LLM fine-tuning.",
        "achievements": [
            "Architected YouTube AI RAG system with ChromaDB and Groq Llama 3.3 70B, reducing transcript analysis time by 80%.",
            "Developed FastMCP tools for AI agent integrations (Cursor, Claude Desktop, Antigravity) supporting automated tool use.",
            "Engineered end-to-end FastAPI microservices serving real-time vector retrieval and LLM responses."
        ],
        "technologies": ["Python", "FastAPI", "RAG", "LangChain", "ChromaDB", "Llama 3.3 70B", "Groq", "MCP", "Docker"]
    },
    {
        "company": "Smart India Hackathon (SIH)",
        "role": "SIH National Finalist & Lead AI Developer",
        "type": "Hackathon",
        "start_date": "2025",
        "end_date": "2026",
        "year": "2025 - 2026",
        "period": "2025 - 2026",
        "location": "Ministry of Education / Campus",
        "description": "Selected twice by IIIT Bhagalpur to represent the institute at the Smart India Hackathon national competition, building transactional data pipelines and Power BI dashboards.",
        "achievements": [
            "Selected twice by IIIT Bhagalpur for national-level SIH hackathons in both 2025 and 2026.",
            "Processed 25M+ rows of customer transaction data using SQL and Pandas to uncover churn risks.",
            "Designed executive Power BI & Tableau dashboards with automated refresh pipelines connected to PostgreSQL data warehouses."
        ],
        "technologies": ["Python", "SQL", "PostgreSQL", "Pandas", "Power BI", "Tableau", "FastAPI"]
    },
    {
        "company": "National Data Science & AI Hackathon",
        "role": "1st Place Winner & Lead AI Developer",
        "type": "Hackathon",
        "start_date": "2025",
        "end_date": "2025",
        "year": "2025",
        "period": "2025",
        "location": "National Competition",
        "description": "Built a real-time predictive analytics & automated forecasting engine during 48-hour intensive hackathon.",
        "achievements": [
            "Awarded 1st place among 120+ participant teams for innovative automated ML & time-series forecasting pipeline.",
            "Engineered an interactive Streamlit application displaying real-time anomaly detection and predictive alerts."
        ],
        "technologies": ["Python", "Prophet", "Streamlit", "XGBoost", "FastAPI", "Plotly", "Git"]
    },
    {
        "company": "IIIT Bhagalpur Hackathon",
        "role": "Top 10 Rank & AI Solution Architect",
        "type": "Hackathon",
        "start_date": "2025",
        "end_date": "2025",
        "year": "2025",
        "period": "2025",
        "location": "IIIT Bhagalpur",
        "description": "Participated in an intra-college hackathon with 500+ participants and secured a Top 10 position building deep neural network vision models.",
        "achievements": [
            "Secured Top 10 position among 500+ participants in intra-college hackathon competition.",
            "Trained computer vision defect inspection models using PyTorch and YOLOv8 operating at 35 FPS.",
            "Implemented SHAP model interpretability dashboards for complex ensemble machine learning classifiers."
        ],
        "technologies": ["Python", "PyTorch", "YOLOv8", "Scikit-Learn", "SHAP", "OpenCV", "Pandas", "Matplotlib"]
    }
]
