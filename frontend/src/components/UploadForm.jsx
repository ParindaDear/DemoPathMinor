import { useState } from "react"; 
import axios from "axios";

export default function UploadForm() {
    const [file, setFile] = useState(null);
    const [text, setText] = useState("");
    const [entities, setEntities] = useState([]);
    const [reportUrl, setReportUrl] = useState("");

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);
        const res = await axios.post("http://localhost:8000/upload/", formData);
        setText(res.data.text);
        setEntities(res.data.entities);
        setReportUrl(`http://localhost:8000${res.data.report_url}`);
    };

    return (
        <div>
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>

            {text && (
                <>
                    <h3>OCR Text:</h3>
                    <pre>{text}</pre>

                    <h3>Entities:</h3>
                    <ul>
                        {entities.map((ent, idx) => (
                            <li key={idx}>
                                <strong>{ent.text}</strong> ({ent.label}, source: {ent.source})
                            </li>
                        ))}
                    </ul>

                    {reportUrl && (
                        <a href={reportUrl} download>
                            <button>Download Report PDF</button>
                        </a>
                    )}
                </>
            )}
        </div>
    );
}
