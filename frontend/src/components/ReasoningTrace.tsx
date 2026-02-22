"use client";

import { ChevronDown, ChevronRight, Bot } from "lucide-react";
import { useState } from "react";
import type { AnalyzeResponse, ReasonStep } from "@/lib/api";

export function ReasoningTrace({ trace }: { trace: AnalyzeResponse["reasoning_trace"] }) {
    const [open, setOpen] = useState(false);
    if (!trace || trace.length === 0) return null;

    return (
        <div className="glass rounded-xl overflow-hidden">
            <button
                onClick={() => setOpen(!open)}
                className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors"
            >
                <div className="flex items-center gap-2 text-sm font-medium">
                    <Bot className="h-4 w-4 text-violet-400" />
                    <span>Reasoning Trace</span>
                    <span className="text-xs text-muted-foreground px-2 py-0.5 rounded-full bg-muted/50">
                        {trace.length} steps
                    </span>
                </div>
                {open
                    ? <ChevronDown className="h-4 w-4 text-muted-foreground" />
                    : <ChevronRight className="h-4 w-4 text-muted-foreground" />
                }
            </button>

            {open && (
                <div className="border-t border-border/50 divide-y divide-border/30">
                    {trace.map((step: ReasonStep, i: number) => (
                        <div key={i} className="p-4 text-sm">
                            <div className="flex items-center gap-2 mb-1.5">
                                <span className="text-xs font-mono text-muted-foreground w-5 text-center">
                                    {i + 1}
                                </span>
                                <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 capitalize">
                                    {step.agent}
                                </span>
                                <span className="text-xs text-muted-foreground capitalize">{step.action}</span>
                            </div>
                            {step.details && Object.keys(step.details).length > 0 && (
                                <div className="ml-7 text-muted-foreground space-y-0.5">
                                    {Object.entries(step.details).slice(0, 3).map(([k, v]) => (
                                        <p key={k} className="line-clamp-2 text-xs">
                                            <span className="text-foreground/50">{k}: </span>{String(v)}
                                        </p>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
