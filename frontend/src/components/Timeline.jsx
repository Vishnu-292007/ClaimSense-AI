function Timeline({ verification }) {
  if (!verification) return null;

  return (
    <div className="card full">
      <h2>📋 Verification Timeline</h2>

      <ul className="timeline">
        {verification.checks.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default Timeline;
