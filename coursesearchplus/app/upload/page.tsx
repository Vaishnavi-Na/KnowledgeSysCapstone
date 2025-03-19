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
  // Add state for tracking drag events
  const [isDragActive, setIsDragActive] = useState<boolean>(false);

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

  // Handle drag events
  const handleDrag = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  };
  
  // Handle dropped file
  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      // Check if the file is a PDF
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
        setMessage('');
      } else {
        setMessage('Please upload a PDF file');
      }
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
          <div className="mt-10 mb-8">
            <div className="max-w-xl mx-auto">
              {/* File Drop Zone with drag and drop handlers */}
              <label
                htmlFor="file-upload" 
                className={`block cursor-pointer border-2 border-dashed rounded-lg p-8 transition-colors 
                  ${file ? 'border-green-400 bg-green-50' : 
                    isDragActive ? 'border-red-500 bg-red-50' : 'border-gray-300 hover:border-red-400'}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="text-center">
                  {!file ? (
                    <>
                      <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-600">
                        <span className="font-medium text-red-600 hover:text-red-500">
                          Click to browse
                        </span> or drag and drop
                      </p>
                      <p className="mt-1 text-xs text-gray-500">PDF only (max 10MB)</p>
                    </>
                  ) : (
                    <>
                      <svg xmlns="http://www.w3.org/2000/svg" className="mx-auto h-12 w-12 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p className="mt-2 text-sm text-gray-600">File selected:</p>
                      <p className="mt-1 text-sm font-medium text-gray-900">{file.name}</p>
                      <button 
                        type="button"
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          setFile(null);
                        }} 
                        className="mt-2 px-3 py-1 text-xs text-red-500 hover:text-white hover:bg-red-500 border border-red-500 rounded-full transition-colors"
                      >
                        Remove file
                      </button>
                    </>
                  )}
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    accept=".pdf"
                    className="sr-only"
                    onChange={handleFileChange}
                  />
                </div>
              </label>
              
              {/* Upload button (removed Browse Files button) */}
              <div className="mt-6 flex justify-center">
                <button
                  onClick={handleSubmit}
                  disabled={uploading || !file}
                  className={`inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm text-white 
                    ${!file ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500'}`}
                >
                  {uploading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </>
                  ) : (
                    'Upload Transcript'
                  )}
                </button>
              </div>
              
              {/* Message display */}
              {message && (
                <div className={`mt-4 p-3 rounded-md ${message.includes('successfully') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                  <div className="flex">
                    <div className="flex-shrink-0">
                      {message.includes('successfully') ? (
                        <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium">{message}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
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
