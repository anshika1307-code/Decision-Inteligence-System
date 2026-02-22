"use client";

import { useState } from "react";
import { analyzeQuery, type AnalyzeRequest, type AnalyzeResponse } from "@/lib/api";

export function useAnalyze() {
    const [result, setResult] = useState<AnalyzeResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [elapsedTime, setElapsedTime] = useState<number>(0);

    const analyze = async (request: AnalyzeRequest) => {
        setLoading(true);
        setError(null);
        setResult(null);
        const start = Date.now();

        const timer = setInterval(() => {
            setElapsedTime(Math.floor((Date.now() - start) / 1000));
        }, 1000);

        try {
            const data = await analyzeQuery(request);
            if (data.error) {
                setError(data.error);
            } else {
                setResult(data);
            }
        } catch (err: unknown) {
            const msg =
                err instanceof Error
                    ? err.message
                    : "Failed to connect to backend. Is it running on port 8000?";
            setError(msg);
        } finally {
            clearInterval(timer);
            setElapsedTime(0);
            setLoading(false);
        }
    };

    return { result, loading, error, elapsedTime, analyze };
}
