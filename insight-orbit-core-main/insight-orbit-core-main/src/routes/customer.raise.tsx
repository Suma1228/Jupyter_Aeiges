import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { Send, Paperclip, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { useState, useRef } from "react";
import api from "@/lib/api/client";

export const Route = createFileRoute("/customer/raise")({
  head: () => ({ meta: [{ title: "Raise Complaint — Aegis" }] }),
  component: RaiseComplaint,
});

// Matches your FastAPI complaint schema
interface ComplaintPayload {
  policy_number: string;
  category: string;
  title: string;
  description: string;
}

type Status = "idle" | "loading" | "success" | "error";

function RaiseComplaint() {
  const [status, setStatus] = useState<Status>("idle");
  const [errorMsg, setErrorMsg] = useState("");
  const [complaintId, setComplaintId] = useState<string | null>(null);

  // Controlled form state
  const [form, setForm] = useState<ComplaintPayload>({
    policy_number: "",
    category: "Claim handling",
    title: "",
    description: "",
  });

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileNames, setFileNames] = useState<string[]>([]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? []);
    setFileNames(files.map((f) => f.name));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");

    try {
      const res = await api.post("/api/complaints", form);
      console.log("CREATE RESPONSE:", res.data);
      setComplaintId(res.data?.id ?? res.data?.complaint_id ?? null);
      setStatus("success");
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Failed to submit complaint. Please try again.";
      setErrorMsg(msg);
      setStatus("error");
    }
  };

  // ── Success state ──────────────────────────────────────────────────────────
  if (status === "success") {
    return (
      <AppShell
        role="customer"
        title="Raise Complaint"
        subtitle="Tell us what happened. Our AI triage will assign and route within seconds."
      >
        <GlassPanel className="mx-auto max-w-3xl p-8 sm:p-10">
          <div className="flex flex-col items-center gap-4 py-6 text-center">
            <div className="grid h-16 w-16 place-items-center rounded-2xl bg-primary/15 ring-1 ring-primary/30">
              <CheckCircle2 className="h-8 w-8 text-primary" />
            </div>
            <div>
              <h2 className="font-display text-xl font-semibold text-foreground">
                Complaint submitted
              </h2>
              <p className="mt-1 text-sm text-muted-foreground">
                AI triage is running. You'll receive a status update shortly.
              </p>
              {complaintId && (
                <p className="mt-3 font-mono text-xs text-muted-foreground">
                  Reference ID:{" "}
                  <span className="text-primary">{complaintId}</span>
                </p>
              )}
            </div>
            <button
              onClick={() => {
                setStatus("idle");
                setForm({ policy_number: "", category: "Claim handling", title: "", description: "" });
                setFileNames([]);
              }}
              className="mt-2 rounded-xl border border-border bg-secondary px-5 py-2.5 text-sm font-medium text-foreground transition hover:bg-accent"
            >
              Raise another complaint
            </button>
          </div>
        </GlassPanel>
      </AppShell>
    );
  }

  // ── Form state ─────────────────────────────────────────────────────────────
  return (
    <AppShell
      role="customer"
      title="Raise Complaint"
      subtitle="Tell us what happened. Our AI triage will assign and route within seconds."
    >
      <GlassPanel className="mx-auto max-w-3xl p-6 sm:p-8">
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <FormField label="Policy number">
              <input
                name="policy_number"
                type="text"
                required
                value={form.policy_number}
                onChange={handleChange}
                placeholder="POL-XXXXX"
                className="form-input"
              />
            </FormField>

            <FormField label="Category">
              <select
                name="category"
                value={form.category}
                onChange={handleChange}
                className="form-input"
              >
                <option>Claim handling</option>
                <option>Billing &amp; payments</option>
                <option>Coverage dispute</option>
                <option>Agent conduct</option>
                <option>Other</option>
              </select>
            </FormField>
          </div>

          <FormField label="Subject">
            <input
              name="title"
              type="text"
              required
              value={form.title}
              onChange={handleChange}
              placeholder="Short summary of the issue"
              className="form-input"
            />
          </FormField>

          <FormField label="Describe what happened">
            <textarea
              name="description"
              required
              rows={6}
              value={form.description}
              onChange={handleChange}
              placeholder="Provide as much detail as possible — dates, amounts, and people involved."
              className="form-input resize-none"
            />
          </FormField>

          <FormField label="Attachments">
            <label className="flex cursor-pointer flex-col gap-2 rounded-xl border border-dashed border-border bg-input/30 px-4 py-5 text-sm text-muted-foreground transition hover:border-primary/40 hover:text-foreground">
              <div className="flex items-center gap-3">
                <Paperclip className="h-4 w-4" />
                {fileNames.length === 0
                  ? "Drag & drop files, or click to browse"
                  : `${fileNames.length} file(s) selected`}
              </div>
              {fileNames.length > 0 && (
                <ul className="ml-7 space-y-0.5">
                  {fileNames.map((n) => (
                    <li key={n} className="font-mono text-[11px] text-primary truncate">{n}</li>
                  ))}
                </ul>
              )}
              <input
                ref={fileInputRef}
                type="file"
                multiple
                className="hidden"
                onChange={handleFileChange}
              />
            </label>
          </FormField>

          {/* Error banner */}
          {status === "error" && (
            <div className="flex items-center gap-2 rounded-xl border border-destructive/30 bg-destructive/10 px-3.5 py-2.5">
              <AlertCircle className="h-4 w-4 shrink-0 text-destructive" />
              <p className="text-sm text-destructive">{errorMsg}</p>
            </div>
          )}

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={() => {
                setForm({ policy_number: "", category: "Claim handling", title: "", description: "" });
                setFileNames([]);
                setStatus("idle");
              }}
              className="rounded-xl border border-border bg-secondary px-4 py-2.5 text-sm font-medium text-foreground transition hover:bg-accent"
            >
              Clear
            </button>

            <button
              type="submit"
              disabled={status === "loading"}
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground transition hover:opacity-90 glow-ring disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {status === "loading" ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Submitting…
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Submit complaint
                </>
              )}
            </button>
          </div>
        </form>
      </GlassPanel>

      <style>{`
        .form-input {
          width: 100%;
          border-radius: 0.75rem;
          border: 1px solid var(--color-border);
          background: oklch(1 0 0 / 0.04);
          padding: 0.7rem 0.9rem;
          font-size: 0.875rem;
          color: var(--color-foreground);
        }
        .form-input::placeholder { color: var(--color-muted-foreground); }
        .form-input:focus { outline: none; border-color: oklch(0.72 0.18 230 / 0.6); box-shadow: 0 0 0 3px oklch(0.72 0.18 230 / 0.25); }
      `}</style>
    </AppShell>
  );
}

function FormField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <span className="mb-1.5 block font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
        {label}
      </span>
      {children}
    </label>
  );
}