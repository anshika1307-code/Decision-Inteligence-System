# Multi-Agent Decision Intelligence System – Architecture

---

# 1. System Architecture Overview

```mermaid
flowchart TD

Client[Client Applications]

subgraph Client Layer
REST[REST API Client]
end

subgraph API_Gateway_Layer["API Gateway Layer"]
FastAPI[FastAPI Server]
Auth[Authentication]
RateLimit[Rate Limiter]
Validator[Input Validator]
end

subgraph Orchestration_Layer["Orchestration Layer"]
Supervisor[Supervisor Agent]
Classifier[Query Classifier]
Router[Workflow Router]
end

subgraph Agent_Layer["Agent Layer"]
Research[Research Agent]
Risk[Risk Agent]
Financial[Financial Agent]
FactCheck[Fact Check Agent]
Summary[Summary Agent]
end

subgraph Retrieval_Layer["Retrieval Layer"]
Hybrid[Hybrid Retrieval Engine]
VectorDB[Vector DB - Qdrant]
BM25[BM25 Search]
Reranker[Reranker]
MetaFilter[Metadata Filter]
end

subgraph Data_Layer["Data Layer"]
Redis[Redis Cache]
Postgres[PostgreSQL]
S3[S3 Storage]
end

subgraph LLM_Layer["LLM Layer"]
OpenAI[OpenAI API]
Anthropic[Anthropic API]
Embeddings[Embedding Service]
end

subgraph Observability["Observability Layer"]
Logger[Loguru Logger]
Prometheus[Prometheus Metrics]
LangSmith[LangSmith / LangFuse]
RAGAS[RAGAS Evaluator]
end

Client --> REST
REST --> FastAPI
FastAPI --> Auth
FastAPI --> RateLimit
FastAPI --> Validator

FastAPI --> Supervisor
Supervisor --> Classifier
Classifier --> Router

Router --> Research
Router --> Risk
Router --> Financial

Research --> Hybrid
Risk --> Hybrid
Financial --> Hybrid

Hybrid --> VectorDB
Hybrid --> BM25
Hybrid --> Reranker
Hybrid --> MetaFilter

Research --> OpenAI
Risk --> OpenAI
Financial --> OpenAI
FactCheck --> Anthropic
Summary --> OpenAI

Supervisor --> Redis
Supervisor --> Postgres
Supervisor --> S3

Supervisor --> Logger
Supervisor --> Prometheus
Supervisor --> LangSmith
Supervisor --> RAGAS
```
# 2. Component Details

## 2.1 Supervisor Agent

The Supervisor Agent is the central orchestrator that manages the entire decision intelligence workflow. It uses LangGraph to create a stateful, multi-agent system that can handle complex business queries.

### Responsibilities

- **Query Understanding**: Analyzes the user's query to determine the intent and required information
- **Workflow Routing**: Selects the appropriate agent workflow based on query complexity and domain
- **Agent Coordination**: Manages the execution order of specialized agents
- **State Management**: Maintains the overall state of the decision-making process
- **Result Aggregation**: Combines outputs from multiple agents into a comprehensive decision report
- **Quality Control**: Ensures all agents complete their tasks and maintains data consistency

### Workflow

```mermaid
flowchart TD

A[Query Input]
B[Classify Query]
C[Plan Workflow]
D[Execute Agents]
E[Validate Results]
F{Need Retry?}
G[Aggregate Results]
H[Generate Report]
I[Return Report]

A --> B
B --> C
C --> D
D --> E
E --> F
F -- Yes --> D
F -- No --> G
G --> H
H --> I
```
# 2.2 Research Agent

```mermaid
flowchart TD

Start[Start Research Task]

subgraph Research_Agent["Research Agent"]
Plan[Plan Research Strategy]
Search[Execute Hybrid Search]
Analyze[Analyze Search Results]
Synthesize[Synthesize Findings]
Format[Format Research Report]
End[Return Research Data]
end

Start --> Plan
Plan --> Search
Search --> Analyze
Analyze --> Synthesize
Synthesize --> Format
Format --> End
```

# 2.3 Risk Agent

```mermaid
flowchart TD

Start[Start Risk Assessment]

subgraph Risk_Agent["Risk Agent"]
Identify[Identify Risk Factors]
Analyze[Analyze Risk Impact]
Evaluate[Evaluate Risk Probability]
Mitigate[Develop Mitigation Strategies]
Format[Format Risk Report]
End[Return Risk Analysis]
end

Start --> Identify
Identify --> Analyze
Analyze --> Evaluate
Evaluate --> Mitigate
Mitigate --> Format
Format --> End
```
# 2.4 Financial Agent

```mermaid
flowchart TD

Start[Start Financial Analysis]

subgraph Financial_Agent["Financial Agent"]
AnalyzeMarket[Analyze Market Data]
EvaluateInvestment[Evaluate Investment Opportunities]
AssessFinancial[Assess Financial Impact]
Forecast[Generate Financial Forecasts]
Format[Format Financial Report]
End[Return Financial Analysis]
end

Start --> AnalyzeMarket
AnalyzeMarket --> EvaluateInvestment
EvaluateInvestment --> AssessFinancial
AssessFinancial --> Forecast
Forecast --> Format
Format --> End
```
# 2.5 Fact Check Agent

```mermaid
flowchart TD

Start[Start Fact-Checking Process]

subgraph FactCheck_Agent["Fact Check Agent"]
Verify[Verify Claims]
CrossReference[Cross-Reference Sources]
Detect[Detect Inconsistencies]
Evaluate[Evaluate Credibility]
Format[Format Fact-Check Report]
End[Return Fact-Check Results]
end

Start --> Verify
Verify --> CrossReference
CrossReference --> Detect
Detect --> Evaluate
Evaluate --> Format
Format --> End
```
# 2.6 Summary Agent

```mermaid
flowchart TD

Start[Start Summary Generation]

subgraph Summary_Agent["Summary Agent"]
Extract[Extract Key Information]
Summarize[Generate Summary]
Highlight[Highlight Key Insights]
Format[Format Summary Report]
End[Return Summary]
end

Start --> Extract
Extract --> Summarize
Summarize --> Highlight
Highlight --> Format
Format --> End
```
# 2.7 Hybrid Retrieval Engine

```mermaid
flowchart TD

Start[Start Retrieval Process]

subgraph Hybrid_Retrieval["Hybrid Retrieval Engine"]
ParseQuery[Parse Query]
VectorSearch[Vector Search]
BM25Search[BM25 Search]
Combine[Combine Results]
Rerank[Rerank Results]
Filter[Filter Results]
End[Return Retrieved Documents]
end

Start --> ParseQuery
ParseQuery --> VectorSearch
ParseQuery --> BM25Search
VectorSearch --> Combine
BM25Search --> Combine
Combine --> Rerank
Rerank --> Filter
Filter --> End
```
# 2.8 Observability Layer

```mermaid
flowchart TD

Start[Start Observability]

subgraph Observability_Layer["Observability Layer"]
Logger[Loguru Logger]
Metrics[Prometheus Metrics]
Tracing[LangSmith / LangFuse]
RAGAS[RAGAS Evaluator]
End[Return Observability Data]
end

Start --> Logger
Logger --> Metrics
Metrics --> Tracing
Tracing --> RAGAS
RAGAS --> End
```
# 3. Data Flow Diagrams

## 3.1 Overall System Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant API_Gateway as API Gateway
    participant Supervisor
    participant Research
    participant Risk
    participant Financial
    participant Hybrid_Retrieval as Hybrid Retrieval
    participant VectorDB
    participant BM25
    participant Reranker
    participant OpenAI
    participant Redis
    participant Postgres
    participant S3
    participant Prometheus
    participant LangSmith

    Client->>API_Gateway: POST /api/v1/analyze
    API_Gateway->>Supervisor: Analyze Query
    Supervisor->>Supervisor: Parse and Classify
    Supervisor->>Redis: Check Cache
    
    alt Cache Hit
        Redis-->>Supervisor: Cached Results
        Supervisor-->>API_Gateway: Return Cached Response
        API_Gateway-->>Client: Decision Report
    else Cache Miss
        Redis-->>Supervisor: No Cache
        
        Supervisor->>Research: Research Task
        Supervisor->>Risk: Risk Task
        Supervisor->>Financial: Financial Task
        
        Research->>Hybrid_Retrieval: Search Documents
        Risk->>Hybrid_Retrieval: Search Documents
        Financial->>Hybrid_Retrieval: Search Documents
        
        Hybrid_Retrieval->>VectorDB: Vector Search
        Hybrid_Retrieval->>BM25: Keyword Search
        VectorDB-->>Hybrid_Retrieval: Vector Results
        BM25-->>Hybrid_Retrieval: BM25 Results
        
        Hybrid_Retrieval->>Reranker: Rerank Results
        Reranker-->>Hybrid_Retrieval: Reranked Results
        
        Hybrid_Retrieval-->>Research: Retrieved Documents
        Hybrid_Retrieval-->>Risk: Retrieved Documents
        Hybrid_Retrieval-->>Financial: Retrieved Documents
        
        Research->>OpenAI: Analyze Research
        Risk->>OpenAI: Analyze Risk
        Financial->>OpenAI: Analyze Financials
        
        OpenAI-->>Research: Research Analysis
        OpenAI-->>Risk: Risk Analysis
        OpenAI-->>Financial: Financial Analysis
        
        Research-->>Supervisor: Research Results
        Risk-->>Supervisor: Risk Results
        Financial-->>Supervisor: Financial Results
        
        Supervisor->>Supervisor: Aggregate Results
        Supervisor->>Postgres: Save Results
        Supervisor->>S3: Save Artifacts
        Supervisor->>Redis: Cache Results
        
        Supervisor->>Prometheus: Log Metrics
        Supervisor->>LangSmith: Log Trace
        
        Supervisor-->>API_Gateway: Decision Report
        API_Gateway-->>Client: Decision Report
    end
```
