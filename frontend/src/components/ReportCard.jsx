function ReportCard({ report }) {
  if (!report) return null;

  return (
    <div className="card full">
      <h2>🤖 AI Verification Report</h2>

      <div className="report">{report}</div>
    </div>
  );
}

export default ReportCard;
