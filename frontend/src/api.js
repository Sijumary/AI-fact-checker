import axios from "axios";

const API = "http://localhost:8000";

export const uploadImage = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/analyze-image`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
    });

    return res.data;
};
