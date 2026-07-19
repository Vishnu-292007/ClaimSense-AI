function UploadCard({ files, setFiles, uploadFile }) {
  return (
    <div className="card">
      <h2>📤 Upload Documents</h2>

      <input
        type="file"
        multiple
        accept=".pdf,.jpg,.jpeg,.png"
        onChange={(e) => setFiles([...files, ...Array.from(e.target.files)])}
      />

      <button
        onClick={() => {
          console.log("Upload button clicked");
          uploadFile();
        }}
      >
        Upload Documents
      </button>

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
    </div>
  );
}

export default UploadCard;
