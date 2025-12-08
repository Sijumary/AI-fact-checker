import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("image"); // "image" or "video"
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    const type = e.target.files[0].type;
    setFileType(type.startsWith("video") ? "video" : "image");
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const endpoint =
        fileType === "image"
          ? "http://localhost:8000/analyze-image"
          : "http://localhost:8000/analyze-video";

      const response = await axios.post(endpoint, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert("Error analyzing file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "20px auto", fontFamily: "sans-serif" }}>
      <h1>AI Fact Checker</h1>

      <input type="file" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        disabled={!file || loading}
        style={{ marginLeft: "10px", padding: "5px 10px" }}
      >
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>

      {result && fileType === "image" && (
        <div style={{ marginTop: "20px" }}>
          <h2>Image Analysis Result</h2>
          <p><strong>File ID:</strong> {result.file_id}</p>
          <p><strong>AI Detection:</strong> {result.ai_detection.result} ({result.ai_detection.confidence})</p>
          <p><strong>ELA Score:</strong> {result.ela_score}</p>
          <p><strong>EXIF Data:</strong></p>
          <pre style={{ background: "#eee", padding: "10px" }}>{JSON.stringify(result.exif, null, 2)}</pre>
          <img src={result.ela_image_url} alt="ELA result" style={{ maxWidth: "100%" }} />
        </div>
      )}

      {result && fileType === "video" && (
        <div style={{ marginTop: "20px" }}>
          <h2>Video Analysis Result</h2>
          <p><strong>Video ID:</strong> {result.video_id}</p>
          <p><strong>Result:</strong> {result.video_detection.result}</p>
          <p><strong>Confidence:</strong> {result.video_detection.confidence}</p>
          <p><strong>Frames Checked:</strong> {result.video_detection.frames_checked}</p>
          <p><strong>Fake Frames:</strong> {result.video_detection.fake_frames}</p>
          <p><strong>Real Frames:</strong> {result.video_detection.real_frames}</p>
        </div>
      )}
    </div>
  );
}

export default App;
