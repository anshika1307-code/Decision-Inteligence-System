import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
    baseURL: `${API_BASE}/api/v1`,
    timeout: 120000,
    headers: { "Content-Type": "application/json" },
});

// --- Request models (must match backend exactly) ---

export type AnalysisDepth = "quick" | "standard" | "comprehensive";

export interface QueryOptions {
    depth?: AnalysisDepth;
    include_reasoning?: boolean;
    max_sources?: number;
    force_refresh?: boolean;
}

export interface AnalyzeRequest {
    query: string;         // min_length=10
    options?: QueryOptions;
}

// --- Response models ---

export interface Classification {
    primary_category: string;
    confidence: number;
    entities: Record<string, unknown>;
}

export interface ReasonStep {
    agent: string;
    action: string;
    timestamp: number;
    details: Record<string, unknown>;
}

export interface AnalyzeResponse {
    query: string;
    classification: Classification | null;
    executive_summary: string | null;
    detailed_analysis: Record<string, unknown> | null;
    risk_summary: string | null;
    financial_overview: string | null;
    recommendations: string[] | null;
    confidence_score: number | null;
    reasoning_trace: ReasonStep[] | null;
    metadata: {
        processing_time?: number;
        agent_plan?: string[];
        total_cost_usd?: number;
        tokens_used?: number;
        [key: string]: unknown;
    };
    error: string | null;
}

export interface HealthResponse {
    status: string;
    version: string;
}

// --- API calls ---

export const analyzeQuery = async (data: AnalyzeRequest): Promise<AnalyzeResponse> => {
    const res = await api.post<AnalyzeResponse>("/analyze", data);
    return res.data;
};

export const getHealth = async (): Promise<HealthResponse> => {
    const res = await api.get<HealthResponse>("/health");
    return res.data;
};

export const getMetrics = async (): Promise<Record<string, unknown>> => {
    const res = await api.get("/metrics");
    return res.data;
};
