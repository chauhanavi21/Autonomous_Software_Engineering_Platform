"use client";

import { useMemo, useState } from "react";
import { Activity, Bot, BrainCircuit, ShieldCheck, TerminalSquare } from "lucide-react";

type AgentCard = {
  role: string;
  title: string;
  description: string;
  icon: typeof Bot;
};

const agents: AgentCard[] = [
  {
    role: "architect",
    title: "Architect Agent",
    description: "Turns requirements into service boundaries, data models, risks, and implementation plans.",
    icon: BrainCircuit,
  },
  {
    role: "backend",
    title: "Backend Engineer",
    description: "Designs API, persistence, reliability, and testable backend implementation steps.",
    icon: TerminalSquare,
  },
  {
    role: "qa",
    title: "QA Agent",
    description: "Builds unit, integration, edge-case, failure-mode, and regression test strategies.",
    icon: ShieldCheck,
  },
];

export default function AgentConsolePage() {
  const [selected, setSelected] = useState("architect");
  const active = useMemo(() => agents.find((agent) => agent.role === selected)!, [selected]);
  const Icon = active.icon;

  return (
    <main className="min-h-screen bg-black px-8 py-10 text-white">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 flex items-start justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-neutral-500">ForgeOS / Agent Runtime</p>
            <h1 className="mt-3 text-4xl font-semibold tracking-tight">Engineering Agents</h1>
            <p className="mt-3 max-w-2xl text-neutral-400">
              Configure provider-independent engineering agents, execute them against project context,
              and inspect the resulting telemetry.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-300">
            <Activity size={15} /> Runtime ready
          </div>
        </div>

        <div className="grid gap-5 lg:grid-cols-[360px_1fr]">
          <section className="space-y-3">
            {agents.map((agent) => {
              const AgentIcon = agent.icon;
              const isSelected = agent.role === selected;
              return (
                <button
                  key={agent.role}
                  onClick={() => setSelected(agent.role)}
                  className={`w-full rounded-xl border p-5 text-left transition ${
                    isSelected ? "border-white/25 bg-white/10" : "border-white/10 bg-white/[0.03] hover:bg-white/[0.06]"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <AgentIcon size={20} />
                    <span className="font-medium">{agent.title}</span>
                  </div>
                  <p className="mt-3 text-sm leading-6 text-neutral-500">{agent.description}</p>
                </button>
              );
            })}
          </section>

          <section className="rounded-xl border border-white/10 bg-white/[0.03] p-7">
            <div className="flex items-center gap-3">
              <div className="rounded-lg border border-white/10 bg-white/5 p-3"><Icon size={22} /></div>
              <div>
                <h2 className="text-xl font-medium">{active.title}</h2>
                <p className="text-sm text-neutral-500">role: {active.role}</p>
              </div>
            </div>

            <div className="mt-8 grid gap-4 md:grid-cols-4">
              {[
                ["Provider", "Mock / configurable"],
                ["Budget", "4,000 tokens"],
                ["Timeout", "60 seconds"],
                ["Telemetry", "Persisted"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-lg border border-white/10 p-4">
                  <p className="text-xs uppercase tracking-wider text-neutral-600">{label}</p>
                  <p className="mt-2 text-sm text-neutral-300">{value}</p>
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-xl border border-white/10 bg-black p-5 font-mono text-sm text-neutral-400">
              <p className="text-neutral-600">$ forgeos agent execute --role {active.role}</p>
              <p className="mt-3">waiting for project input...</p>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}
