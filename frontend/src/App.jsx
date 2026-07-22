import { useState } from "react";
import axios from "axios";

import "./App.css";

import Navbar from "./components/Navbar";
import UploadCard from "./components/UploadCard";
import ClaimSummary from "./components/ClaimSummary";
import RiskCard from "./components/RiskCard";
import DecisionCard from "./components/DecisionCard";
import Timeline from "./components/Timeline";
import ReportCard from "./components/ReportCard";
import ChatBot from "./components/ChatBot";

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [claimData, setClaimData] = useState(null);
  const [verification, setVerification] = useState(null);
  const [report, setReport] = useState("");

  const uploadFile = async () => {
    if (files.length === 0) {
      alert("Please select one or more documents.");
      return;
    }

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await axios.post(
        "https://claimsense-ai-production-4698.up.railway.app/upload",
        formData,
      );

      setClaimData(response.data.claim_data);
      setVerification(response.data.verification);
      setReport(response.data.report);

      alert("Documents uploaded successfully!");
    } catch (err) {
      console.log(err);
      console.log(err.response);
      console.log(err.response?.data);

      alert("Upload Failed");
    }
  };

  const askAI = async () => {
    if (!question) return;

    try {
      const response = await axios.post(
        "https://claimsense-ai-production-4698.up.railway.app/ask",
        {
          question,
        },
      );

      setAnswer(response.data.answer);
    } catch (err) {
      console.error(err);
      alert("AI request failed");
    }
  };

  return (
    <div className="app">
      <Navbar />

      <div className="container">
        <div className="grid">
          <UploadCard
            files={files}
            setFiles={setFiles}
            uploadFile={uploadFile}
          />

          <ClaimSummary claimData={claimData} />

          <RiskCard verification={verification} />

          <DecisionCard verification={verification} />

          <Timeline verification={verification} />

          <ReportCard report={report} />

          <ChatBot
            question={question}
            setQuestion={setQuestion}
            askAI={askAI}
            answer={answer}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
