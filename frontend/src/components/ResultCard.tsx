"use client";

import { Badge } from "@/components/ui/badge";
import { CheckCircle2, AlertTriangle, TrendingUp, FileSearch, Brain, AlignLeft, BarChart3 } from "lucide-react";
import type { AnalyzeResponse } from "@/lib/api";

export function ResultCard({ result }: { result: AnalyzeResponse }) {
    const confidencePct = result.confidence_score != null
        ? Math.round(result.confidence_score * 100)
        : null;

    const category = result.classification?.primary_category ?? "Unknown";
    const classConfidence = result.classification?.confidence ?? null;

    return (
        <div className="space-y-4 animate-slide-up">
            {/* Executive Summary */}
            <div className="glass rounded-2xl p-6 gradient-border">
                <div className="flex items-start justify-between gap-4 mb-4 flex-wrap">
                    <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-5 w-5 text-green-400 flex-shrink-0" />
                        <h3 className="font-semibold text-lg">Executive Summary</h3>
                    </div>
                    <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant="secondary" className="capitalize">{category}</Badge>
                        {classConfidence != null && (
                            <span className="text-xs text-muted-foreground">
                                {Math.round(classConfidence * 100)}% category confidence
                            </span>
                        )}
                        {confidencePct != null && (
                            <div
                                className="flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full"
                                style={{
                                    background: `hsl(${confidencePct > 70 ? "142 76% 55%" : "38 92% 55%"} / 0.15)`,
                                    color: `hsl(${confidencePct > 70 ? "142 76% 55%" : "38 92% 55%"})`,
                                }}
                            >
                                <div
                                    className="h-1.5 w-1.5 rounded-full animate-pulse"
                                    style={{ background: `hsl(${confidencePct > 70 ? "142 76% 55%" : "38 92% 55%"})` }}
                                />
                                {confidencePct}% confidence
                            </div>
                        )}
                    </div>
                </div>
                <p className="text-foreground/90 leading-relaxed">
                    {result.executive_summary ?? "Analysis complete. See details below."}
                </p>
            </div>

            {/* Detailed Analysis Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {result.detailed_analysis && (
                    <div className="glass rounded-xl p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <div className="p-1.5 rounded-lg bg-blue-500/10">
                                <TrendingUp className="h-4 w-4 text-blue-400" />
                            </div>
                            <span className="font-medium text-sm">Research Analysis</span>
                        </div>
                        <div className="text-sm text-muted-foreground space-y-1">
                            {Object.entries(result.detailed_analysis).slice(0, 4).map(([k, v]) => (
                                <div key={k} className="flex gap-2">
                                    <span className="capitalize text-foreground/60 flex-shrink-0 min-w-[80px]">
                                        {k.replace(/_/g, " ")}:
                                    </span>
                                    <span className="line-clamp-2">{String(v)}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {result.risk_summary && (
                    <div className="glass rounded-xl p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <div className="p-1.5 rounded-lg bg-red-500/10">
                                <AlertTriangle className="h-4 w-4 text-red-400" />
                            </div>
                            <span className="font-medium text-sm">Risk Assessment</span>
                        </div>
                        <p className="text-sm text-muted-foreground line-clamp-5">{result.risk_summary}</p>
                    </div>
                )}

                {result.financial_overview && (
                    <div className="glass rounded-xl p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <div className="p-1.5 rounded-lg bg-green-500/10">
                                <BarChart3 className="h-4 w-4 text-green-400" />
                            </div>
                            <span className="font-medium text-sm">Financial Overview</span>
                        </div>
                        <p className="text-sm text-muted-foreground line-clamp-5">{result.financial_overview}</p>
                    </div>
                )}

                {result.recommendations && result.recommendations.length > 0 && (
                    <div className="glass rounded-xl p-4">
                        <div className="flex items-center gap-2 mb-3">
                            <div className="p-1.5 rounded-lg bg-violet-500/10">
                                <AlignLeft className="h-4 w-4 text-violet-400" />
                            </div>
                            <span className="font-medium text-sm">Recommendations</span>
                        </div>
                        <ul className="space-y-1.5">
                            {result.recommendations.slice(0, 4).map((rec, i) => (
                                <li key={i} className="text-sm text-muted-foreground flex gap-2">
                                    <span className="text-violet-400 flex-shrink-0 font-bold">{i + 1}.</span>
                                    <span className="line-clamp-2">{rec}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Metadata Strip */}
            <div className="glass rounded-xl p-4 flex flex-wrap gap-6 text-sm">
                {result.metadata?.processing_time != null && (
                    <div>
                        <span className="text-muted-foreground text-xs block mb-0.5">Processing Time</span>
                        <p className="font-semibold text-blue-400">
                            {Number(result.metadata.processing_time).toFixed(1)}s
                        </p>
                    </div>
                )}
                {result.metadata?.total_cost_usd != null && (
                    <div>
                        <span className="text-muted-foreground text-xs block mb-0.5">Cost</span>
                        <p className="font-semibold text-green-400">
                            ${Number(result.metadata.total_cost_usd).toFixed(4)}
                        </p>
                    </div>
                )}
                {result.metadata?.tokens_used != null && (
                    <div>
                        <span className="text-muted-foreground text-xs block mb-0.5">Tokens</span>
                        <p className="font-semibold text-violet-400">
                            {Number(result.metadata.tokens_used).toLocaleString()}
                        </p>
                    </div>
                )}
                {result.metadata?.agent_plan && (
                    <div>
                        <span className="text-muted-foreground text-xs block mb-0.5">Agents Used</span>
                        <p className="font-semibold text-cyan-400">
                            {(result.metadata.agent_plan as string[]).length}
                        </p>
                    </div>
                )}
                <div>
                    <span className="text-muted-foreground text-xs block mb-0.5">Category</span>
                    <p className="font-semibold text-orange-400 capitalize">{category}</p>
                </div>
            </div>
        </div>
    );
}
