'use client';

import Link from 'next/link';
import NavbarElse from '@/components/navbarElse';

export default function SearchPage() {
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        {/* Main Content */}
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold mb-6">Course Search</h1>

          {/* Search Section */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold mb-4">Search for Courses</h2>
            <p className="text-lg leading-relaxed mb-6">
              Find the perfect courses based on your preferences. Search by course number, 
              professor name, or keywords to discover detailed information about classes 
              at Ohio State University.
            </p>
            
            {/* Search Input */}
            <div className="flex gap-4">
              <input 
                type="text"
                placeholder="Search courses..."
                className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500"
              />
              <button className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition-colors">
                Search
              </button>
            </div>
          </section>

          {/* Removed Back to Home Link */}
        </div>
      </main>
    </>
  );
}
