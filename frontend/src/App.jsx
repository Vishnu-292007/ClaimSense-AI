import { useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [claimData, setClaimData] = useState(null);
  const [verification, setVerification] = useState(null);
  const [report, setReport] = useState("");

  const uploadFile = async () => {
    alert("Upload started");

    if (files.length === 0) {
      alert("Please select one or more PDFs");
      return;
    }

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
      );

      setClaimData(response.data.claim_data);
      setVerification(response.data.verification);
      setReport(response.data.report);

      console.log(response.data.uploaded_files);

      alert(
        "Uploaded Files:\n" +
          response.data.uploaded_files.join("\n") +
          "\n\nText:\n" +
          response.data.text,
      );
    } catch (error) {
      console.error(error);
      alert("Upload Failed");
    }
  };

  const askAI = async () => {
    if (!question) {
      alert("Please enter a question");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question: question,
      });

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      alert("Failed to get AI answer");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>ClaimSense AI</h1>

      <input
        type="file"
        multiple
        accept=".pdf,.jpg,.jpeg,.png"
        onChange={(e) => {
          setFiles((prev) => [...prev, ...Array.from(e.target.files)]);
        }}
      />

      <br />
      <br />

      <button onClick={uploadFile}>Upload</button>

      <br />
      <br />

      <input
        type="text"
        placeholder="Ask about the uploaded documents..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askAI}>Ask AI</button>

      <br />
      <br />

      {files.length > 0 && (
        <>
          <h3>Selected Files</h3>

          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </>
      )}

      {claimData && (
        <>
          <h2>Extracted Claim Details</h2>

          <p>
            <b>Claim ID:</b> {claimData.claim_id}
          </p>

          <p>
            <b>Customer:</b> {claimData.customer_name}
          </p>

          <p>
            <b>Policy:</b> {claimData.policy_number}
          </p>

          <p>
            <b>Hospital:</b> {claimData.hospital || "Not Found"}
          </p>

          <p>
            <b>Claim Amount:</b> {claimData.claim_amount}
          </p>

          <p>
            <b>Incident Date:</b> {claimData.incident_date}
          </p>

          <p>
            <b>Status:</b> {claimData.status}
          </p>

          <p>
            <b>Reason:</b> {claimData.reason}
          </p>
        </>
      )}

      {verification && (
        <>
          <h2>Verification Report</h2>

          <h3>{verification.overall_status}</h3>

          <h2>{verification.decision}</h2>

          <ul>
            {verification.checks.map((check, index) => (
              <li key={index}>{check}</li>
            ))}
          </ul>
        </>
      )}

      {report && (
        <>
          <h2>AI Verification Report</h2>

          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "8px",
              padding: "15px",
              marginTop: "20px",
              background: "#f9f9f9",
              whiteSpace: "pre-wrap",
            }}
          >
            {report}
          </div>
        </>
      )}

      {answer && (
        <>
          <h2>AI Answer</h2>

          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "8px",
              padding: "15px",
              marginTop: "20px",
              background: "#eef6ff",
              whiteSpace: "pre-wrap",
            }}
          >
            {answer}
          </div>
        </>
      )}
    </div>
  );
}

export default App;
