import { jwtDecode } from "jwt-decode";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import {
  ShieldCheck, User2, Headset, ArrowRight,
  Sparkles, Lock, AlertCircle, Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Sign in — Aegis Insurance Operations" },
      {
        name: "description",
        content: "Sign in to the Aegis AI insurance complaint platform.",
      },
    ],
  }),
  component: LoginPage,
});

type Persona = "customer" | "ops";

// ─── FIXED AUTH REQUEST ─────────────────────────────────────────────
async function loginRequest(email: string, password: string) {
  const res = await fetch("https://notebooks.amd.com/jupyter-hack-team-2671-260612052841-847ec4b2/proxy/8002/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail ?? "Invalid credentials");
  }

  return res.json() as Promise<{
    access_token: string;
    token_type: string;
    role: string;
  }>;
}
// ─────────────────────────────────────────────────────────────

function LoginPage() {
  const navigate = useNavigate();
  const [persona, setPersona] = useState<Persona>("customer");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [agentId, setAgentId] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setError(null);
  setLoading(true);

  try {
    const data = await loginRequest(email, password);

    localStorage.setItem("access_token", data.access_token);

    // ✅ decode JWT to get role
    const decoded: any = jwtDecode(data.access_token);

    const role = decoded.role; // "CUSTOMER" or "OPS"

    localStorage.setItem("user_role", role);

    const destination =
      role === "OPS" ? "/ops" : "/customer";

    navigate({ to: destination });

  } catch (err: unknown) {
    setError(err instanceof Error ? err.message : "Something went wrong");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-10">

      {/* UI unchanged */}
      <div className="relative z-10 grid w-full max-w-5xl gap-8 lg:grid-cols-2">

        {/* LEFT PANEL (UNCHANGED) */}
        <div className="hidden flex-col justify-between p-2 lg:flex">
          <Link to="/" className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-primary to-accent glow-ring">
              <ShieldCheck className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <p className="font-display text-xl font-semibold tracking-tight">Aegis</p>
              <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted-foreground">
                AI Complaint Operations
              </p>
            </div>
          </Link>
        </div>

        {/* RIGHT PANEL */}
        <div className="glass-strong rounded-3xl p-7 sm:p-9">

          <h1 className="font-display text-2xl font-semibold tracking-tight">
            Welcome back
          </h1>

          <p className="mt-1 text-sm text-muted-foreground">
            Select your workspace and sign in.
          </p>

          {/* FORM */}
          <form onSubmit={handleSubmit} className="mt-6 space-y-4">

            <Field label="Email">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-xl border px-3.5 py-2.5 text-sm"
              />
            </Field>

            <Field label="Password">
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full rounded-xl border py-2.5 pl-10 pr-3 text-sm"
                />
              </div>
            </Field>

            {/* ERROR */}
            {error && (
              <div className="flex items-center gap-2 rounded-xl border border-red-400 bg-red-50 px-3 py-2">
                <AlertCircle className="h-4 w-4 text-red-500" />
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            {/* BUTTON */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-primary py-2.5 text-white"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Signing in...
                </span>
              ) : (
                "Login"
              )}
            </button>

          </form>
        </div>
      </div>
    </div>
  );
}

// ── unchanged components ──
function Field({ label, children }: any) {
  return (
    <label className="block">
      <div className="mb-1 text-xs uppercase text-muted-foreground">
        {label}
      </div>
      {children}
    </label>
  );
}