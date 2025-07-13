import { useState } from "react"; 
import axios from "axios";

export default function UploadForm() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState("");

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);
        const res = await axios.post("http://localhost:8000/upload/", formData);
        setResult(res.data.text);
    };

    return (
        <div>
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>
            <pre>{result}</pre>
        </div>
    );
}