function RiskCard({ verification }) {
  if (!verification?.risk_analysis) return null;

  const risk = verification.risk_analysis;

  let color = "#16a34a";

  if (risk.risk_level === "MEDIUM RISK") color = "#ca8a04";

  if (risk.risk_level === "HIGH RISK") color = "#dc2626";

  return (
    <div className="card">
      <h2>📊 Risk Analysis</h2>

      <h1
        style={{
          color,
          fontSize: "50px",
        }}
      >
        {risk.risk_score}
      </h1>

      <h3 style={{ color }}>{risk.risk_level}</h3>

      <br />

      <ul>
        {risk.reasons.map((reason, i) => (
          <li key={i}>{reason}</li>
        ))}
      </ul>
    </div>
  );
}

export default RiskCard;
