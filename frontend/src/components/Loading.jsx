/**
 * Loading — Reusable loading spinner / skeleton component
 */
export default function Loading({ text = 'Generating with AI...' }) {
  return (
    <div className="loading">
      <div className="loading-spinner"></div>
      <p>{text}</p>
    </div>
  );
}
