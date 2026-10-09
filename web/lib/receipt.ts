export type ReceiptEvidence = {
  [key: string]: unknown;
  ticker?: string;
  provider?: string;
  representation?: string;
  market_status?: string | null;
  reference_age_status?: string;
  reference_price_updated_at?: string | null;
  token_price_updated_at?: string | null;
  eligibility_status?: string | null;
  token_to_share_ratio?: string | null;
  price_impact_percent?: string | null;
  quote_observed_at?: string | null;
  quote_available?: boolean;
  simulation_passed?: boolean;
};
export type ReceiptData = {
  [key: string]: unknown;
  origin?: string;
  disclosure?: string;
  action?: string;
  receipt: {
    [key: string]: unknown;
    decision: string;
    evidence: ReceiptEvidence;
    intent: { [key: string]: unknown; notional_usd?: string; ticker?: string };
    mandate?: { [key: string]: unknown; max_notional_usd?: string };
    policy_version?: string;
    timestamp?: string;
    reason_codes: string[];
    receipt_sha256: string;
  };
  view?: { [key: string]: unknown; representation?: string; route?: string };
};
export function canonicalize(
  value: unknown,
  excludeReceiptHash = false,
): unknown {
  if (Array.isArray(value)) return value.map((item) => canonicalize(item));
  if (value && typeof value === "object")
    return Object.keys(value as Record<string, unknown>)
      .sort()
      .reduce<Record<string, unknown>>(
        (out, key) => {
          if (excludeReceiptHash && key === "receipt_sha256") return out;
          out[key] = canonicalize((value as Record<string, unknown>)[key]);
          return out;
        },
        Object.create(null) as Record<string, unknown>,
      );
  return value;
}
export async function digestReceipt(data: ReceiptData): Promise<string> {
  if (!globalThis.crypto?.subtle)
    throw new Error("Web Crypto SHA-256 is unavailable.");
  const bytes = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(JSON.stringify(canonicalize(data.receipt, true))),
  );
  return Array.from(new Uint8Array(bytes), (byte) =>
    byte.toString(16).padStart(2, "0"),
  ).join("");
}
export async function verifyReceipt(data: ReceiptData): Promise<boolean> {
  return (await digestReceipt(data)) === data.receipt.receipt_sha256;
}
