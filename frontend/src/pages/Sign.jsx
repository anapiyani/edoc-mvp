import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getDocumentByToken,
  getDocumentFileUrl,
  submitDecision,
} from "../api/api";
import "./Sign.css";

function StatusBadge({ status }) {
  const modifier =
    status === "accepted"
      ? "sign-badge--accepted"
      : status === "rejected"
        ? "sign-badge--rejected"
        : "sign-badge--awaiting";
  return (
    <span className={`sign-badge ${modifier}`}>{status.replace("_", " ")}</span>
  );
}

function IconCheck() {
  return (
    <svg
      className="sign-icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function IconX() {
  return (
    <svg
      className="sign-icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

function IconDownload() {
  return (
    <svg
      className="sign-icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  );
}

function IconFile() {
  return (
    <svg
      className="sign-icon"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  );
}

function IconAlert() {
  return (
    <svg
      className="sign-icon"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function Spinner() {
  return (
    <svg
      className="sign-icon sign-spinner"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
  );
}

export default function Sign() {
  const { token } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [decisionLoading, setDecisionLoading] = useState(false);
  const [decisionMessage, setDecisionMessage] = useState(null);

  useEffect(() => {
    if (!token) return;
    setLoading(true);
    setError(null);
    getDocumentByToken(token)
      .then(setData)
      .catch((e) => setError(e.message || "Failed to load document"))
      .finally(() => setLoading(false));
  }, [token]);

  const fileUrl = token ? getDocumentFileUrl(token) : null;
  const canDecide = data?.status === "awaiting_decision";

  const handleDecision = async (decision) => {
    if (!token || !canDecide) return;
    setDecisionLoading(true);
    setDecisionMessage(null);
    try {
      const result = await submitDecision(token, decision);
      setData((prev) => (prev ? { ...prev, status: result.status } : null));
      setDecisionMessage(
        result.status === "accepted"
          ? "Document accepted."
          : "Document rejected.",
      );
    } catch (e) {
      setDecisionMessage(e.message || "Request failed.");
    } finally {
      setDecisionLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="sign-page">
        <div className="sign-container">
          <div className="sign-message sign-message--error">
            <IconAlert />
            <span>Missing document token.</span>
          </div>
        </div>
      </div>
    );
  }

  const isMessageError =
    decisionMessage &&
    !decisionMessage.startsWith("Document accepted") &&
    !decisionMessage.startsWith("Document rejected");

  return (
    <div className="sign-page">
      <div className="sign-container">
        <header className="sign-header">
          <h1 className="sign-title">Sign document</h1>
          <p className="sign-subtitle">
            Review the PDF below, then accept or reject.
          </p>
        </header>

        {/* PDF shown immediately when page opens – no wait for document info */}
        <section className="sign-card sign-pdf-wrap">
          <iframe
            title="Document PDF"
            className="sign-pdf-iframe"
            src={fileUrl}
          />
        </section>

        {loading ? (
          <div className="sign-card sign-loading">
            <div className="sign-skeleton" />
            <div className="sign-skeleton" />
            <div className="sign-skeleton" />
          </div>
        ) : error ? (
          <div className="sign-message sign-message--error">
            <IconAlert />
            <span>{error}</span>
          </div>
        ) : data ? (
          <>
            <section className="sign-card">
              <div className="sign-card-title">
                <IconFile />
                <span>Document info</span>
              </div>
              <div className="sign-grid">
                <div className="sign-field">
                  <span className="sign-label">Deal ID</span>
                  <span className="sign-value">{data.deal_id}</span>
                </div>
                <div className="sign-field">
                  <span className="sign-label">Doc ID</span>
                  <span className="sign-value">{data.doc_id}</span>
                </div>
                <div className="sign-field">
                  <span className="sign-label">Status</span>
                  <StatusBadge status={data.status} />
                </div>
                {data.full_name && (
                  <div className="sign-field">
                    <span className="sign-label">Full name</span>
                    <span className="sign-value">{data.full_name}</span>
                  </div>
                )}
                {data.iin && (
                  <div className="sign-field">
                    <span className="sign-label">IIN</span>
                    <span className="sign-value">{data.iin}</span>
                  </div>
                )}
              </div>
            </section>

            {decisionMessage && (
              <div
                className={
                  isMessageError
                    ? "sign-message sign-message--error"
                    : "sign-message sign-message--success"
                }
              >
                {isMessageError ? <IconAlert /> : <IconCheck />}
                <span>{decisionMessage}</span>
              </div>
            )}

            <div className="sign-actions">
              <a
                href={fileUrl}
                download="document.pdf"
                className="sign-btn sign-btn--outline"
              >
                <IconDownload />
                <span>Download PDF</span>
              </a>
              <button
                type="button"
                className="sign-btn sign-btn--primary"
                onClick={() => handleDecision("accepted")}
                disabled={!canDecide || decisionLoading}
              >
                {decisionLoading ? <Spinner /> : <IconCheck />}
                <span>Accept</span>
              </button>
              <button
                type="button"
                className="sign-btn sign-btn--danger"
                onClick={() => handleDecision("rejected")}
                disabled={!canDecide || decisionLoading}
              >
                {decisionLoading ? <Spinner /> : <IconX />}
                <span>Reject</span>
              </button>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}
