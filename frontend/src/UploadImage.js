import './App.css';
import React , { useState } from 'react';
import AWS from 'aws-sdk';

const S3_BUCKET ='b2-photo-store';
const REGION ='us-east-1';

const AWS_ACCESS_KEY_ID = process.env.REACT_APP_AWS_ACCESS_KEY_ID;
const AWS_SECRET_ACCESS_KEY = process.env.REACT_APP_AWS_SECRET_ACCESS_KEY;

AWS.config.update({
    accessKeyId: AWS_ACCESS_KEY_ID,
    secretAccessKey: AWS_SECRET_ACCESS_KEY
})

const myBucket = new AWS.S3({
    params: { Bucket: S3_BUCKET },
    region: REGION,
})

const UploadImage = () => {
    const [progress , setProgress] = useState(0);
    const [selectedFile, setSelectedFile] = useState(null);
    const [labels, setLabels] = useState("");

    const handleFileInput = (e) => {
        setSelectedFile(e.target.files[0]);
    }

    const uploadFile = (file) => {

        const params = {
            ACL: 'public-read',
            Body: file,
            Bucket: S3_BUCKET,
            Key: file.name,
            Metadata: {'customLabels': labels }
        };

        let req = myBucket.putObject(params)
                
        req.on('httpUploadProgress', (evt) => {
            setProgress(Math.round((evt.loaded / evt.total) * 100))
        })
        req.send((err) => {
            if (err) {
                console.log(err) 
            } else {
                console.log(req);
            }
        })
    }

    return (
    <div>
        <div className="container">
            <div className="upload">
                <label>Labels:</label>
                <input value={labels} onInput={e => setLabels(e.target.value)}/>
                </div>
        </div>
        <div className="upload-button-container">
            <input type="file" onChange={handleFileInput}/>
            <button onClick={() => uploadFile(selectedFile)}>Upload</button>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2px'}}>
                Upload Progress: {progress}%
        </div>
    </div>
    )
}

export default UploadImage;