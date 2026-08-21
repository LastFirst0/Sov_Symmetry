declare global { interface Window { __sovIngestionToken?: string } }

/** Ephemeral owner token only; it is deliberately not written to local or session storage. */
export function setIngestionToken(token: string) { window.__sovIngestionToken = token; }
export function clearIngestionToken() { delete window.__sovIngestionToken; }
export function getIngestionToken() { return window.__sovIngestionToken; }
