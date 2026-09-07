"use client";

import { useEffect, useState } from "react";

import type { ReadyHealthResponse } from "@/lib/api";
import { getHealth } from "@/lib/api";

export function HealthCard() {
  const [health, setHealth] = useState<ReadyHealthResponse | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setFailed(true));
  }, []);

  if (failed) {
    return (
      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 text-sm text-neutral-400">
        API is not ready yet. Start the Docker stack and run the migration.
      </div>
    );
  }

  if (!health) {
    return (
      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5 text-sm text-neutral-400">
        Checking platform readiness…
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm text-neutral-400">Platform readiness</span>
        <span className="rounded-full border border-white/10 px-3 py-1 text-xs">
          {health.status}
        </span>
      </div>
      <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-xl bg-white/[0.04] p-3">PostgreSQL: {health.database.status}</div>
        <div className="rounded-xl bg-white/[0.04] p-3">Redis: {health.redis.status}</div>
      </div>
    </div>
  );
}
