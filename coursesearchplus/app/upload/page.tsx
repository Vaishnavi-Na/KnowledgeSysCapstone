'use client';

import Link from 'next/link';
import NavbarElse from '@/components/navbarElse';
import React, { useState, useEffect } from 'react';
import './search.css';

const server_endpoint = 'http://localhost:8000'

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>('');
  const [retreived, setRetreived] = useState<boolean>(false);
  const [transcript, setTranscript] = useState<{ special: string; courses: string[] }>({
    special: 'None',
    courses: ['None'],
  });

  // // Pull existing transcript from local storage if it exists
  // var tempTranscript = localStorage.getItem("transcript");
  // if (tempTranscript !== null) {
  //   setTranscript(JSON.parse(tempTranscript));
  //   //setRetreived(true);
  // }
  useEffect(() => {
    if (typeof window !== "undefined") {
      const tempTranscript = localStorage.getItem("transcript");
      if (tempTranscript !== null) {
        setTranscript(JSON.parse(tempTranscript));
        setRetreived(true);
      }
    }
  }, []);

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  // Handle form submission (upload)
  const handleSubmit = async () => {
    if (!file) {
      setMessage('Missing a file to upload!');
      return;
    }
    // Make sure the uploaded file is a pdf
    if (file.type !== 'application/pdf') {
      setMessage('Please upload a pdf!');
      return;
    }

    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${server_endpoint}/upload`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`File uploaded successfully!`);
        setTranscript(result);
        setRetreived(true);

        // Add transcript to localstorage
        localStorage.setItem("transcript", JSON.stringify(result));
      } 
      else {
        setMessage(`Error: ${result.error}`);
      }
    } 
    catch (error) {
      setMessage(`Error handling submit: ${error}`);
    } 
    finally {
      setUploading(false);
    }
  };

  // Function to chunk the data into groups of 5
  const chunkArray = (arr: string[], size: number) => {
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
      chunks.push(arr.slice(i, i + size));
    }
    return chunks;
  };
  const rows = chunkArray(transcript.courses, 5); // Split the list into rows of 5
  
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        {/* Header */}
        
        {/* Main Content */}
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold mb-6">Upload Your Transcript</h1>

          {/* Instructions */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold mb-4">How to Get Your Transcript</h2>
            <ol className="list-decimal pl-6 text-lg leading-relaxed">
              <li>Go to <a href="https://buckeyelink.osu.edu/" target="_blank" className="text-blue-500 underline">Buckeyelink</a>.</li>
              <li>Click on <strong>"Request Advising Report"</strong>.</li>
              <li>Select the appropriate academic term and submit the request.</li>
              <li>Once generated, download the transcript as a PDF file.</li>
              <li>Upload the file below.</li>
            </ol>
          </section>

          {/* File Upload */}
          <div className="mt-10">
            <label htmlFor="file-upload" className="cursor-pointer bg-red-500 text-white py-3 px-6 rounded-lg shadow-md flex items-center space-x-2 hover:bg-red-600">
              <div>
                <input type="file" onChange={handleFileChange} />
                <button onClick={handleSubmit} disabled={uploading}>
                  {uploading ? 'Uploading...' : 'Upload Transcript'}
                </button>
                {message && <p>{message}</p>}
              </div>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 10a1 1 0 011-1h3V4a1 1 0 112 0v5h3a1 1 0 110 2h-3v5a1 1 0 11-2 0v-5H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
            </label>
            {/* No file input or state needed */}
          </div>

          {/* Table view of transcript */}
          {retreived && 
            <table>
              <caption> <strong> Courses Taken </strong> </caption>
              <tbody> 
                {rows.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((item, colIndex) => (
                      <td key={colIndex} className="border border-gray-300 p-2">
                        {item}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          }

          {/* Back to Home Link */}
          <div className="mt-12">
            <Link href="/" className="text-foreground hover:underline text-lg">
              ← Back to Home
            </Link>
          </div>
        </div>
      </main>
    </>
  );
}
