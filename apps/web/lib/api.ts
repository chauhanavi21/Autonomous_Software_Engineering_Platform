const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export interface ComponentHealth {
  status: "healthy" | "unhealthy";
  latency_ms?: number | null;
}

export interface ReadyHealthResponse {
  status: "healthy" | "degraded";
  service: string;
  database: ComponentHealth;
  redis: ComponentHealth;
}

export async function getHealth(): Promise<ReadyHealthResponse> {
  const response = await fetch(`${API_URL}/health/ready`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`ForgeOS API returned ${response.status}`);
  }
  return response.json();
}
