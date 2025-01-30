'use client';

import Link from 'next/link';

export default function UploadPage() {
  return (
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

        {/* File Upload (Visual Only) */}
        <div className="mt-10">
          <label htmlFor="file-upload" className="cursor-pointer bg-red-500 text-white py-3 px-6 rounded-lg shadow-md flex items-center space-x-2 hover:bg-red-600">
            <span>Upload Transcript</span>
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 10a1 1 0 011-1h3V4a1 1 0 112 0v5h3a1 1 0 110 2h-3v5a1 1 0 11-2 0v-5H4a1 1 0 01-1-1z" clipRule="evenodd" />
            </svg>
          </label>
          {/* No file input or state needed */}
        </div>

        {/* Back to Home Link */}
        <div className="mt-12">
          <Link href="/" className="text-foreground hover:underline text-lg">
            ← Back to Home
          </Link>
        </div>
      </div>
    </main>
  );
}
