import { Activity, ArrowRight, Box, GitBranch, Network, Terminal } from "lucide-react";

import { HealthCard } from "@/components/health-card";

const capabilities = [
  [Network, "Multi-Agent Orchestration", "Coordinate specialized engineering agents through dependency-aware workflows."],
  [GitBranch, "Engineering Lifecycle", "Move from planning and architecture to implementation, review and deployment."],
  [Terminal, "Secure Execution", "Prepare for isolated execution with explicit resource and runtime boundaries."],
  [Activity, "Full Observability", "Trace requests, dependencies, failures, latency and future agent execution."],
] as const;

export default function Home() {
  return (
    <main className="min-h-screen text-white">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/15 bg-white/[0.06]">
            <Box size={19} />
          </div>
          <span className="font-semibold tracking-tight">ForgeOS</span>
        </div>
        <span className="text-sm text-neutral-500">Phase 1 / Foundation</span>
      </nav>

      <section className="mx-auto grid max-w-7xl gap-14 px-6 pb-16 pt-24 lg:grid-cols-[1.4fr_0.6fr] lg:px-8 lg:pt-32">
        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-neutral-300">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            Engineering intelligence, orchestrated.
          </div>
          <h1 className="max-w-5xl text-6xl font-semibold tracking-[-0.055em] md:text-8xl">
            Build software like an organization.
          </h1>
          <p className="mt-8 max-w-2xl text-lg leading-8 text-neutral-400 md:text-xl">
            ForgeOS is the foundation for an autonomous engineering platform that will coordinate product, architecture, development, testing, review, and operations agents.
          </p>
          <div className="mt-9 flex flex-wrap gap-3">
            <a href="http://localhost:8000/docs" className="flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-medium text-black">
              Explore API <ArrowRight size={16} />
            </a>
            <a href="http://localhost:8000/api/v1/health/ready" className="rounded-xl border border-white/15 px-5 py-3 text-sm text-neutral-300">
              Check readiness
            </a>
          </div>
        </div>
        <div className="self-end">
          <HealthCard />
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl overflow-hidden rounded-2xl border border-white/10 bg-white/10 md:grid-cols-2 lg:grid-cols-4">
        {capabilities.map(([Icon, title, description]) => (
          <div key={title} className="bg-[#050505] p-7">
            <Icon size={21} className="mb-8 text-neutral-400" />
            <h2 className="font-medium">{title}</h2>
            <p className="mt-3 text-sm leading-6 text-neutral-500">{description}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
