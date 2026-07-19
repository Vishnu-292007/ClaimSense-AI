function ClaimSummary({ claimData }) {
  if (!claimData) return null;

  return (
    <div className="card">
      <h2>📄 Claim Summary</h2>

      <p>
        <strong>Claim ID:</strong> {claimData.claim_id}
      </p>
      <p>
        <strong>Customer:</strong> {claimData.customer_name}
      </p>
      <p>
        <strong>Policy:</strong> {claimData.policy_number}
      </p>
      <p>
        <strong>Hospital:</strong> {claimData.hospital || "Not Found"}
      </p>
      <p>
        <strong>Claim Amount:</strong> {claimData.claim_amount}
      </p>
      <p>
        <strong>Date:</strong> {claimData.incident_date}
      </p>
      <p>
        <strong>Reason:</strong> {claimData.reason}
      </p>
    </div>
  );
}

export default ClaimSummary;
