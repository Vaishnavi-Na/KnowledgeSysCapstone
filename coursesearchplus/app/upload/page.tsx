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
  // Add state for manual course entry
  const [newCourse, setNewCourse] = useState<string>('');
  const [showEntryForm, setShowEntryForm] = useState<boolean>(false);
  // Add separate state for course input errors
  const [courseError, setCourseError] = useState<string>('');
  // Add state for course click errors
  const [clickError, setClickError] = useState<string>('');
  // Add state for specialization entry
  const [specialization, setSpecialization] = useState<string>('');
  const [editingSpecialization, setEditingSpecialization] = useState<boolean>(false);

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
        const parsedTranscript = JSON.parse(tempTranscript);
        setTranscript(parsedTranscript);
        // Make sure specialization is empty string unless explicitly set
        setSpecialization(parsedTranscript.special !== 'None' ? parsedTranscript.special : '');
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
        setSpecialization(result.special !== 'None' ? result.special : '');
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
  
  // Handle adding a new course manually
  const handleAddCourse = () => {
    // Clear previous course error
    setCourseError('');
    
    if (!newCourse.trim()) {
      setCourseError('Please enter a valid course code');
      return;
    }
    
    // Format and validate course code
    const trimmedCourse = newCourse.trim();
    
    // Split into department code and course number
    const parts = trimmedCourse.split(/\s+/);
    
    // Validate format: [UPPERCASE LETTERS] [4-DIGIT NUMBER]
    if (parts.length !== 2) {
      setCourseError('Course code must be in the format "DEPT 1234"');
      return;
    }
    
    const deptCode = parts[0];
    const courseNumber = parts[1];
    
    // Check if department code is all uppercase letters
    if (!/^[A-Z]+$/.test(deptCode)) {
      setCourseError('Department code must be all uppercase letters (e.g., CSE)');
      return;
    }
    
    // Check if course number is a 4-digit number
    if (!/^\d{4}$/.test(courseNumber)) {
      setCourseError('Course number must be a 4-digit number (e.g., 3901)');
      return;
    }
    
    // Properly formatted course code
    const formattedCourse = `${deptCode} ${courseNumber}`;
    
    // Check if course already exists in the transcript
    if (transcript.courses.includes(formattedCourse)) {
      setCourseError('This course is already in your transcript');
      return;
    }
    
    // Add the new course to the transcript
    const updatedCourses = [...transcript.courses];
    if (updatedCourses.length === 1 && updatedCourses[0] === 'None') {
      updatedCourses[0] = formattedCourse;
    } else {
      updatedCourses.push(formattedCourse);
    }
    
    const updatedTranscript = {
      ...transcript,
      courses: updatedCourses
    };
    
    setTranscript(updatedTranscript);
    setNewCourse('');
    setMessage('Course added successfully!');
    setRetreived(true);
    
    // Save updated transcript to localStorage
    localStorage.setItem("transcript", JSON.stringify(updatedTranscript));
  };

  // Handle clicking on a course to view details
  const handleCourseClick = async (courseCode: string) => {
    if (courseCode === 'None') return;
    
    setClickError('');
    
    // Split the course code into department and number
    const [dept, num] = courseCode.split(' ');
    
    try {
      // Create search query
      const searchQuery = `${courseCode} Ohio State`;
      const encodedQuery = encodeURIComponent(searchQuery);
      
      // For development purposes, we'll use Google's search directly
      // In production, you might want to replace this with a proper API
      window.open(`https://www.google.com/search?q=${encodedQuery}`, '_blank');
      
      // Note: For a better user experience, you could implement an actual 
      // API endpoint that searches and returns the first valid result URL
      // Then you could navigate directly to that URL instead of the search page
    } catch (error) {
      setClickError(`Error searching for course: ${error}`);
    }
  };

  // Handle saving specialization
  const handleSaveSpecialization = () => {
    // Update transcript with new specialization
    const updatedTranscript = {
      ...transcript,
      special: specialization.trim() || 'None'
    };
    
    setTranscript(updatedTranscript);
    setEditingSpecialization(false);
    
    // Save updated transcript to localStorage
    localStorage.setItem("transcript", JSON.stringify(updatedTranscript));
    
    // Show success message
    setMessage('Major specialization updated successfully!');
  };

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

          {/* After file upload section and before course table */}
          <div className="mt-12 mb-8 w-full">
            {transcript.special !== 'None' ? (
              // Show full academic profile section when a specialization exists
              <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-md">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-2xl font-semibold">Academic Profile</h2>
                  {!editingSpecialization && (
                    <button
                      onClick={() => setEditingSpecialization(true)}
                      className="flex items-center px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
                    >
                      Change Specialization
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                  )}
                </div>
                
                {editingSpecialization ? (
                  <div className="py-2">
                    <div className="flex flex-col md:flex-row gap-4">
                      <div className="flex-grow">
                        <label htmlFor="specialization" className="block text-sm font-medium text-gray-700 mb-1 text-left">
                          Major Specialization (e.g., Artificial Intelligence, Information Systems)
                        </label>
                        <input
                          type="text"
                          id="specialization"
                          value={specialization}
                          onChange={(e) => setSpecialization(e.target.value)}
                          placeholder="Enter your major specialization"
                          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                        />
                      </div>
                      <div className="flex items-end space-x-2">
                        <button
                          onClick={handleSaveSpecialization}
                          className="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => {
                            setEditingSpecialization(false);
                            setSpecialization(transcript.special !== 'None' ? transcript.special : '');
                          }}
                          className="px-6 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:outline-none transition-colors"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="bg-gray-50 p-4 rounded-md">
                    <div className="text-left">
                      <p className="text-sm text-gray-500 mb-1">Major Specialization</p>
                      <p className="text-lg font-medium">
                        {transcript.special}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              // Show just a button when no specialization exists
              <button
                onClick={() => setEditingSpecialization(true)}
                className="w-full py-4 px-6 bg-white border border-gray-200 rounded-lg shadow-md hover:bg-gray-50 text-left flex items-center justify-between"
              >
                <span className="text-lg font-medium text-gray-700">Enter Major Specialization</span>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </button>
            )}
            
            {/* Show the edit form separately when needed but no specialization exists yet */}
            {transcript.special === 'None' && editingSpecialization && (
              <div className="mt-4 bg-white p-6 rounded-lg border border-gray-200 shadow-md">
                <h2 className="text-2xl font-semibold mb-4">Academic Profile</h2>
                <div className="py-2">
                  <div className="flex flex-col md:flex-row gap-4">
                    <div className="flex-grow">
                      <label htmlFor="specialization" className="block text-sm font-medium text-gray-700 mb-1 text-left">
                        Major Specialization (e.g., Artificial Intelligence, Information Systems)
                      </label>
                      <input
                        type="text"
                        id="specialization"
                        value={specialization}
                        onChange={(e) => setSpecialization(e.target.value)}
                        placeholder="Enter your major specialization"
                        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                      />
                    </div>
                    <div className="flex items-end space-x-2">
                      <button
                        onClick={handleSaveSpecialization}
                        className="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingSpecialization(false)}
                        className="px-6 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:outline-none transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
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

          
        </div>
      </main>
    </>
  );
}
