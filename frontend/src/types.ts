// TODO: keep these in sync (by hand) with backend/app/schemas.py

export interface ExtractedEvent {
  id: number;
  title: string;
  start_date: string;
  start_time: string | null;
  end_time: string | null;
  location: string | null;
  description: string | null;
  included: boolean;
  status: "pending_review" | "edited" | "synced" | "sync_failed";
  source_snippet: string | null;
}

export interface SyncResult {
  id: number;
  status: "synced" | "sync_failed";
  google_event_id?: string;
  error?: string;
}

export interface AuthStatus {
  connected: boolean;
  email: string | null;
}
