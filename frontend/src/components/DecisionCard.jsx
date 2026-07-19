function DecisionCard({ verification }) {
  if (!verification?.final_decision) return null;

  const decision = verification.final_decision;

  return (
    <div className="card">
      <h2>🎯 Final Decision</h2>

      <h1>{decision.emoji}</h1>

      <h2>{decision.status}</h2>

      <br />

      <p>{decision.reason}</p>
    </div>
  );
}

export default DecisionCard;
