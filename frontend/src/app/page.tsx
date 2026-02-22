"use client";

import { useState } from "react";
import { Sparkles, Send, Loader2, AlertCircle, Activity, DollarSign, Zap, Brain } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AgentPipeline } from "@/components/AgentPipeline";
import { ResultCard } from "@/components/ResultCard";
import { ReasoningTrace } from "@/components/ReasoningTrace";
import { useAnalyze } from "@/hooks/useAnalyze";
import type { AnalysisDepth } from "@/lib/api";

const EXAMPLE_QUERIES = [
  "Should a B2B SaaS company expand to UAE market in 2026?",
  "What are the key risks of entering the EV market in Southeast Asia?",
  "Analyze the financial viability of launching an AI-powered HR platform.",
  "Compare cloud strategies: AWS vs GCP for an AI-first startup.",
];

const DEPTH_OPTIONS: { value: AnalysisDepth; label: string; desc: string }[] = [
  { value: "quick", label: "Quick", desc: "~10s, classifier + summary" },
  { value: "standard", label: "Standard", desc: "~30s, research + fact-check" },
  { value: "comprehensive", label: "Comprehensive", desc: "~60s, all agents" },
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [depth, setDepth] = useState<AnalysisDepth>("standard");
  const { result, loading, error, elapsedTime, analyze } = useAnalyze();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    await analyze({
      query,
      options: { depth, include_reasoning: true, max_sources: 20 },
    });
  };

  const agentsUsed = result?.metadata?.agent_plan as string[] | undefined;

  return (
    <main className="min-h-screen">
      {/* Header */}
      <div className="relative overflow-hidden border-b border-border/50">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/5 via-transparent to-transparent" />
        <div className="relative max-w-5xl mx-auto px-6 py-12">
          <div className="flex items-center gap-2 mb-4">
            <div className="flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-400 animate-pulse" />
              Multi-Agent AI
            </div>
            <div className="flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full bg-green-500/10 text-green-400 border border-green-500/20">
              <Activity className="h-3 w-3" />
              Live
            </div>
          </div>

          <h1 className="text-4xl md:text-5xl font-bold mb-3 leading-tight">
            <span className="gradient-text">Decision Intelligence</span>
            <br />
            <span className="text-foreground/70 text-3xl md:text-4xl font-semibold">
              AI Analysis Platform
            </span>
          </h1>

          <p className="text-muted-foreground text-lg max-w-2xl mb-8">
            Enterprise-grade strategic decisions powered by 6 specialized AI agents,
            hybrid RAG retrieval, and LangGraph orchestration — at{" "}
            <span className="text-green-400 font-semibold">$0.05/query</span>.
          </p>

          <div className="flex flex-wrap gap-6">
            {[
              { icon: Zap, label: "6 AI Agents", color: "text-blue-400" },
              { icon: DollarSign, label: "$0.05/query", color: "text-green-400" },
              { icon: Brain, label: "Hybrid RAG", color: "text-violet-400" },
              { icon: Activity, label: "LangGraph", color: "text-cyan-400" },
            ].map(({ icon: Icon, label, color }) => (
              <div key={label} className="flex items-center gap-2 text-sm">
                <Icon className={`h-4 w-4 ${color}`} />
                <span className="text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 py-10 space-y-6">

        {/* Query Form */}
        <div className="glass rounded-2xl p-6 gradient-border">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground mb-2 block">
                Strategic Query <span className="text-xs">(min 10 characters)</span>
              </label>
              <Textarea
                id="query-input"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. Should a B2B SaaS startup expand to the UAE market in 2026?"
                className="min-h-[100px] bg-background/50 border-border/50 resize-none text-base focus:border-blue-500/50 transition-all"
                disabled={loading}
              />
            </div>

            {/* Example Queries */}
            <div className="flex flex-wrap gap-2">
              {EXAMPLE_QUERIES.map((q, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setQuery(q)}
                  className="text-xs px-3 py-1.5 rounded-full bg-muted/40 text-muted-foreground hover:bg-blue-500/10 hover:text-blue-400 border border-border/50 hover:border-blue-500/30 transition-all"
                >
                  {q.slice(0, 50)}…
                </button>
              ))}
            </div>

            <div className="flex items-center justify-between gap-4 flex-wrap">
              <div className="flex items-center gap-3">
                <span className="text-sm text-muted-foreground whitespace-nowrap">Analysis Depth:</span>
                <Select value={depth} onValueChange={(v) => setDepth(v as AnalysisDepth)}>
                  <SelectTrigger id="depth-select" className="w-44 bg-background/50 border-border/50">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {DEPTH_OPTIONS.map((opt) => (
                      <SelectItem key={opt.value} value={opt.value}>
                        <span className="font-medium capitalize">{opt.label}</span>
                        <span className="text-muted-foreground ml-2 text-xs">{opt.desc}</span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <Button
                id="analyze-btn"
                type="submit"
                disabled={query.trim().length < 10 || loading}
                className="bg-blue-600 hover:bg-blue-700 text-white glow-blue gap-2 min-w-[140px]"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    {elapsedTime > 0 ? `${elapsedTime}s…` : "Analyzing…"}
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Analyze
                  </>
                )}
              </Button>
            </div>
          </form>
        </div>

        {/* Agent Pipeline */}
        {(loading || result) && (
          <div className="glass rounded-xl p-4">
            <p className="text-xs text-muted-foreground mb-3 uppercase tracking-wider font-medium">
              Agent Pipeline
            </p>
            <AgentPipeline activeAgents={agentsUsed ?? (loading ? ["classifier"] : [])} />
            {loading && (
              <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
                <Loader2 className="h-3 w-3 animate-spin text-blue-400" />
                Running multi-agent analysis{elapsedTime > 0 ? ` (${elapsedTime}s)` : "…"}
              </div>
            )}
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="flex items-start gap-3 p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive animate-fade-in">
            <AlertCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Analysis Failed</p>
              <p className="text-sm mt-0.5 opacity-80">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-4">
            <ResultCard result={result} />
            <ReasoningTrace trace={result.reasoning_trace} />
          </div>
        )}

        {/* Empty State */}
        {!loading && !result && !error && (
          <div className="text-center py-20 text-muted-foreground">
            <div className="mx-auto w-16 h-16 rounded-2xl bg-blue-500/10 flex items-center justify-center mb-4 border border-blue-500/20">
              <Sparkles className="h-8 w-8 text-blue-400" />
            </div>
            <p className="font-medium text-foreground/60">Enter a strategic query above</p>
            <p className="text-sm mt-1 opacity-60">Get a full AI-powered decision report in seconds</p>
          </div>
        )}
      </div>
    </main>
  );
}
