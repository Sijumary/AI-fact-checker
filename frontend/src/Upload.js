import React, { useState } from "react";
import { uploadImage } from "./api";

export default function Upload() {
    const [result, setResult] = useState(null);

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        const res = await uploadImage(file);
        setResult(res);
    };

    return (
        <div style={{ padding: 20 }}>
            <h2>AI Fact-Check: Upload Image</h2>
            <input type="file" onChange={handleUpload} />

            {result && (
                <div style={{ marginTop: 20 }}>
                    <h3>Results:</h3>
                    <pre>{JSON.stringify(result.exif, null, 2)}</pre>

                    <h4>ELA Image:</h4>
                    <img
                        src={result.ela_image_url}
                        alt="ELA result"
                        width="300"
                        style={{ border: "1px solid #999" }}
                    />

                    <h4>ELA Score:</h4>
                    <p>{result.ela_score}</p>
                </div>
            )}
        </div>
    );
}
