"use client";

import { Brain, Zap, Shield, BarChart3 } from "lucide-react";

const agents = [
    { name: "Classifier", icon: Brain, color: "text-blue-400", desc: "Routes query to specialists" },
    { name: "Research", icon: Zap, color: "text-violet-400", desc: "Deep market analysis" },
    { name: "Risk", icon: Shield, color: "text-red-400", desc: "Risk assessment" },
    { name: "Financial", icon: BarChart3, color: "text-green-400", desc: "ROI projections" },
];

export function AgentPipeline({ activeAgents = [] }: { activeAgents?: string[] }) {
    return (
        <div className="flex items-center gap-2 flex-wrap">
            {agents.map((agent, i) => {
                const isActive = activeAgents.some(a => a.toLowerCase().includes(agent.name.toLowerCase()));
                const Icon = agent.icon;
                return (
                    <div key={agent.name} className="flex items-center gap-2">
                        <div
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-500 ${isActive
                                    ? "border-blue-500/50 bg-blue-500/10 text-blue-300 glow-blue"
                                    : "border-border/50 bg-muted/30 text-muted-foreground"
                                }`}
                        >
                            <Icon className={`h-3 w-3 ${isActive ? agent.color : "text-muted-foreground"}`} />
                            {agent.name}
                        </div>
                        {i < agents.length - 1 && (
                            <div className={`h-px w-4 transition-colors duration-500 ${isActive ? "bg-blue-500/50" : "bg-border/30"}`} />
                        )}
                    </div>
                );
            })}
        </div>
    );
}
