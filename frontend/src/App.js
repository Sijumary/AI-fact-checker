import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post(
        "http://localhost:8000/upload-base64",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h2>AI Fact Checker</h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={!selectedFile || loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>EXIF Data</h3>
          <pre
            style={{
              background: "#f0f0f0",
              padding: "10px",
              borderRadius: "5px",
              overflowX: "auto",
            }}
          >
            {JSON.stringify(result.exif, null, 2)}
          </pre>

          <h3>ELA Image</h3>
          {result.ela_base64 ? (
            <img
              src={`data:image/png;base64,${result.ela_base64}`}
              alt="ELA"
              style={{ maxWidth: "100%", border: "1px solid #ccc" }}
            />
          ) : (
            <p>No ELA image generated</p>
          )}
        </div>
      )}
    </div>
  );
}
