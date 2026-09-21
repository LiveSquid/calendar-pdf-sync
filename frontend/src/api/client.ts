// Thin fetch wrapper around the backend API.
// TODO:
//   export async function uploadPdf(file: File): Promise<{ upload_id: number; status: string }>
//   export async function getEventsPreview(uploadId: number): Promise<ExtractedEvent[]>
//   export async function patchEvent(id: number, changes: Partial<ExtractedEvent>): Promise<ExtractedEvent>
//   export async function syncEvents(eventIds: number[]): Promise<SyncResult[]>
//   export async function getAuthStatus(): Promise<AuthStatus>
//
// Base URL should point at the FastAPI backend, e.g. http://localhost:8000
// (consider a Vite dev proxy in vite.config.ts instead of hardcoding it).
