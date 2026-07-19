function ChatBot({ question, setQuestion, askAI, answer }) {
  return (
    <div className="card full">
      <h2>💬 Insurance AI Assistant</h2>

      <input
        type="text"
        placeholder="Ask anything about the uploaded claim..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askAI}>Ask AI</button>

      {answer && (
        <>
          <br />
          <br />

          <div className="report">{answer}</div>
        </>
      )}
    </div>
  );
}

export default ChatBot;
