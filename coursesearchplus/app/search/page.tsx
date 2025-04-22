'use client';

import Link from 'next/link';
import NavbarElse from '@/components/navbarElse';
import { useEffect, useState, useRef } from 'react';

const server_endpoint = 'http://127.0.0.1:8000'

function SendToSearchButton({
  buttonText, 
  onCourseClick, 
  variant = "green", 
}: { 
  buttonText: string; 
  onCourseClick: () => void;
  variant?: "green" | "blue";
}) {
  const baseClasses = "px-4 py-2 rounded-lg transition-colors text-white";
  const colorClasses =
    variant === "green"
      ? "bg-green-500 hover:bg-green-600"
      : "bg-blue-500 hover:bg-blue-600";

  return (
    <button className={`${baseClasses} ${colorClasses}`} onClick={onCourseClick}>
      {buttonText}
    </button>
  );

}

export default function SearchPage() {
  const [remainingGroups, setRemainingGroups] = useState<string[][]>([]);
  const [mainSelectedCourse, setMainSelectedCourse] = useState<string | null>(null); // Main selected course
  const [mainPrereqStructure, setMainPrereqStructure] = useState<string[][]>([]); // Main prereq struc
  const [secondarySelectedCourse, setSecondarySelectedCourse] = useState<string | null>(null); // Secondary selected course
  const [secondaryPrereqStructure, setSecondaryPrereqStructure] = useState<string[][]>([]); // Secondary prereq struc
  const [page, setPage] = useState(0);
  const groupsPerPage = 6;
  const maxPage = Math.ceil(remainingGroups.length / groupsPerPage);
  const pagedGroups = remainingGroups.slice(
    page * groupsPerPage,
    (page + 1) * groupsPerPage
  );
  const [searchInput, setSearchInput] = useState('');
  const [keywordInput, setKeywordInput] = useState('');
  const [sortOption, setSortOption] = useState('avg_rating-desc');
  const [searchResults, setSearchResults] = useState([]); // placeholder to store fetched results
  const [dropdownOpen, setDropdownOpen] = useState(false); // For custom dropdown
  const dropdownRef = useRef<HTMLDivElement>(null); // Ref for dropdown element
  
  // Click outside handler for dropdown
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    }
    
    // Add event listener when dropdown is open
    if (dropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    // Cleanup
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownOpen]);
  
  // Options for our custom dropdown
  const sortOptions = [
    { value: 'sei-desc', label: 'SEI Score ↓' },
    { value: 'sei-asc', label: 'SEI Score ↑' },
    { value: 'avg_rating-desc', label: 'Avg Rating ↓' },
    { value: 'avg_rating-asc', label: 'Avg Rating ↑' },
    { value: 'difficulty-asc', label: 'Difficulty ↑' },
    { value: 'difficulty-desc', label: 'Difficulty ↓' },
    { value: 'comments_relevance-desc', label: 'Comments Relevance ↓' }
  ];
  
  // Get the current selected option label
  const getCurrentSortLabel = () => {
    const option = sortOptions.find(opt => opt.value === sortOption);
    return option ? option.label : 'Select an option';
  };
  
  // Handle option selection
  const handleSortSelect = (value: string) => {
    setSortOption(value);
    setDropdownOpen(false);
  };

  useEffect(() => {
    const transcript = localStorage.getItem('transcript');
    if (transcript) {
      const parsed = JSON.parse(transcript);
      fetch(`${server_endpoint}/courses/get_remain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsed),
      })
        .then(res => res.json())
        .then(data => {
          // console.log('Received from get_remain API:', data);
          setRemainingGroups(data.remaining_groups);
        });
    }
  }, []);

  const handleCourseClick = (course: string) => {
    const transcript = JSON.parse(localStorage.getItem('transcript') || '{}');
    const query = new URLSearchParams({ course }).toString();

    fetch(`${server_endpoint}/courses/calc_remain?${query}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(transcript),
    })
      .then(res => res.json())
      .then(data => {
        setMainSelectedCourse(course);
        // console.log('Received from calc_remain API:', data);
        setMainPrereqStructure(data);
        // Reset secondary course selected
        setSecondarySelectedCourse(null);
        setSecondaryPrereqStructure([])
      });
  };

  const handleSecondaryCourseClick = (course: string) => {
    const transcript = JSON.parse(localStorage.getItem('transcript') || '{}');
    const query = new URLSearchParams({ course }).toString();
  
    fetch(`http://127.0.0.1:8000/courses/calc_remain?${query}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(transcript),
    })
      .then(res => res.json())
      .then(data => {
        setSecondarySelectedCourse(course);
        setSecondaryPrereqStructure(data);
      });
  };

  const handleSearchClick = () => {
    if (!searchInput.includes(" ")) {
      alert("Please enter course in format 'SUBJECT NUMBER' (e.g., CSE 3901)");
      return;
    }

    const [sortBy, order] = sortOption.split("-");
    const query = new URLSearchParams({
      course: searchInput,
      sort_by: sortBy,
      order: order,
      comment_keywords: keywordInput,
    }).toString();
  
    fetch(`http://127.0.0.1:8000/courses/professors_with_courses?${query}`, {
      method: 'POST',
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("Search results:", data);
      setSearchResults(data.matched_professors); 
    })
    .catch((err) => {
      console.error("Search failed:", err);
    });
};

  
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        {/* --- Main Content --- */}
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
            <div className="flex flex-col gap-4">
              {/* Course code input */}
              <input
                type="text"
                value={searchInput}
                onChange={e => setSearchInput(e.target.value)}
                placeholder="Search by course (e.g., CSE 3901)"
                className="p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500"
              />

              {/* Comment keyword input */}
              <input
                type="text"
                value={keywordInput}
                onChange={e => setKeywordInput(e.target.value)}
                placeholder="Keyword in professor reviews (e.g., flipped classroom)"
                className="p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              />

              {/* Custom dropdown - completely rebuilt */}
              <div className="relative z-10" ref={dropdownRef}>
                <button 
                  type="button"
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="w-full flex items-center justify-between bg-white border border-gray-300 rounded-md px-4 py-2.5 text-left text-gray-800 transition-all duration-200 hover:border-red-500 hover:shadow-lg hover:ring-2 hover:ring-red-400/50 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500"
                >
                  <span>{getCurrentSortLabel()}</span>
                  <svg 
                    className={`w-5 h-5 ml-2 transition-transform ${dropdownOpen ? 'transform rotate-180' : ''}`} 
                    viewBox="0 0 20 20" 
                    fill="currentColor"
                  >
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
                
                {dropdownOpen && (
                  <div className="absolute mt-1 w-full rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-20">
                    <div className="py-1 max-h-60 overflow-auto">
                      {sortOptions.map((option) => (
                        <div
                          key={option.value}
                          onClick={() => handleSortSelect(option.value)}
                          className={`${
                            option.value === sortOption 
                              ? 'bg-red-50 text-red-700' 
                              : 'text-gray-800 hover:bg-gray-50 hover:text-red-600'
                          } cursor-pointer select-none relative px-4 py-2 transition-all duration-150 ease-in-out border-l-2 border-transparent hover:border-l-2 hover:border-red-500`}
                        >
                          {option.label}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Search button */}
              <button
                className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors"
                onClick={handleSearchClick}
              >
                Search
              </button>
            </div>
          </section>
        </div>

        {/* Search Results Section */}
        {searchResults.length > 0 && (
          <section className="w-full max-w-screen-xl mx-auto px-8 mt-12">
            <h2 className="text-2xl font-semibold mb-6 text-gray-800">Professors Related to {searchInput}</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {searchResults.map((prof: any, index: number) => (
                <div 
                  key={index} 
                  className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-100 flex flex-col"
                >
                  {/* Header with name */}
                  <div className="bg-gray-700 px-4 py-3">
                    <h3 className="text-lg font-bold truncate text-white">{prof.instructor}</h3>
                    <p className="text-xs text-gray-300">{prof.department}</p>
                  </div>
                  
                  {/* Ratings section */}
                  <div className="grid grid-cols-2 gap-2 p-4 text-sm bg-gray-50">
                    <div className="flex flex-col items-center p-2 rounded-lg bg-white border border-gray-200">
                      <span className="text-xs text-gray-500">Avg Rating</span>
                      <span className={`text-lg font-bold ${getScoreColor(prof.avg_rating)}`}>
                        {prof.avg_rating?.toFixed(2) ?? "N/A"}
                      </span>
                    </div>
                    <div className="flex flex-col items-center p-2 rounded-lg bg-white border border-gray-200">
                      <span className="text-xs text-gray-500">Difficulty</span>
                      <span className={`text-lg font-bold ${getDifficultyColor(prof.difficulty)}`}>
                        {prof.difficulty?.toFixed(2) ?? "N/A"}
                      </span>
                    </div>
                    <div className="flex flex-col items-center p-2 rounded-lg bg-white border border-gray-200">
                      <span className="text-xs text-gray-500">SEI Score</span>
                      <span className={`text-lg font-bold ${getScoreColor(prof.SEI_overall)}`}>
                        {prof.SEI_overall?.toFixed(2) ?? "N/A"}
                      </span>
                    </div>
                    <div className="flex flex-col items-center p-2 rounded-lg bg-white border border-gray-200">
                      <span className="text-xs text-gray-500">Relevance</span>
                      <span className="text-lg font-bold text-red-600">{Number(prof.score).toFixed(2)}</span>
                    </div>
                  </div>
                  <p><strong> When have they taught this class before:</strong></p>
                  <ul className="space-y-1 mt-2">
                    {prof.courses.map((course:any, idx:number) => (
                      <li key={idx} className="text-gray-700">
                        {course.course} {course.time} {course.days} {course.term}
                      </li>
                    ))}
                </ul>
                  {/* Summary comment - full text */}
                  <div className="p-4 text-sm text-gray-600">
                    <p>{prof.summary_comment}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* --- Requirement Group Panel --- */}
        <section className="flex w-full max-w-screen-xl mx-auto gap-6 mt-8 px-8">
          {/* Left: Requirement Groups */}
          <div className="w-3/5">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold">Courses You Can Take</h2>
              <div className="space-x-2">
                <button
                  className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                  disabled={page === 0}
                  onClick={() => setPage(p => Math.max(p - 1, 0))}
                >
                  ◀ Prev
                </button>
                <span className="text-gray-700">
                  Page {page + 1} / {maxPage}
                </span>
                <button
                  className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                  disabled={page >= maxPage - 1}
                  onClick={() => setPage(p => Math.min(p + 1, maxPage - 1))}
                >
                  Next ▶
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {pagedGroups.map((group, idx) => (
                <div key={idx} className="border rounded-lg p-4 shadow bg-white">
                  <h3 className="font-bold mb-2">
                    Requirement Group {page * groupsPerPage + idx + 1}
                  </h3>
                  <div className="flex gap-3 flex-wrap">
                    {group.map(course => (
                      <button
                        key={course}
                        onClick={() => handleCourseClick(course)}
                        className="bg-blue-100 hover:bg-blue-200 px-3 py-1 rounded text-blue-800 text-sm"
                      >
                        {course}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Prerequisites */}
          <div className="w-2/5 bg-yellow-50 rounded-lg p-4 shadow-inner h-full">
            <div className="mb-3">
              <h2 className="text-xl font-semibold">Course Prerequisites</h2>
              {mainSelectedCourse && (
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold">{mainSelectedCourse}</h3>
                  {mainPrereqStructure.length !== 0 && (
                    <SendToSearchButton 
                      buttonText="Send to Search"
                      onCourseClick={() => setSearchInput(mainSelectedCourse)}
                      variant="blue"
                    />
                  )}
              </div>
              )}
            </div>

            <div className="overflow-x-auto mt-2">
              {/* Main selected course panel */}
              {mainSelectedCourse ? (
                <div className="flex gap-4">
                  {mainPrereqStructure.map((orGroup, colIndex) => (
                    <div key={colIndex} className="flex flex-col items-center bg-white p-2 rounded shadow min-w-[120px]">
                      <span className="text-xs text-gray-500 mb-1">AND Group {colIndex + 1}</span>
                      {orGroup.map(course => (
                        <button
                          key={course}
                          onClick={() => handleSecondaryCourseClick(course)}
                          className="bg-red-100 text-red-800 px-2 py-1 rounded mb-1 text-xs text-center"
                        >
                          {course}
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 italic">Click a course to view prerequisites.</p>
              )}

              {/* Secondary selected course panel */}
              {secondarySelectedCourse && (
                <div className="mt-8">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold mb-2">Prerequisites for {secondarySelectedCourse}</h3>
                    {secondaryPrereqStructure.length !== 0 && (
                      <SendToSearchButton 
                        buttonText="Send to Search"
                        onCourseClick={() => setSearchInput(secondarySelectedCourse)}
                        variant="blue"
                      />
                    )}
                  </div>
                  <div className="overflow-x-auto">
                    <div className="flex gap-4">
                      {secondaryPrereqStructure.map((orGroup, colIndex) => (
                        <div key={colIndex} className="flex flex-col items-center bg-white p-2 rounded shadow min-w-[120px]">
                          <span className="text-xs text-gray-500 mb-1">AND Group {colIndex + 1}</span>
                          {orGroup.map(course => (
                            <button
                              key={course}
                              onClick={() => handleSecondaryCourseClick(course)}
                              className="bg-red-100 text-red-800 px-2 py-1 rounded mb-1 text-xs text-center hover:bg-red-200"
                            >
                              {course}
                            </button>
                          ))}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {mainSelectedCourse && mainPrereqStructure.length === 0 && (
                <div className="mt-4">
                  <SendToSearchButton 
                    buttonText={"Ready to Take: "+mainSelectedCourse} 
                    onCourseClick={() => setSearchInput(mainSelectedCourse)}
                  />
                </div>
              )}
              {secondarySelectedCourse && secondaryPrereqStructure.length === 0 && (
                <div className="mt-4">
                  <SendToSearchButton 
                    buttonText={"Ready to Take: "+secondarySelectedCourse} 
                    onCourseClick={() => setSearchInput(secondarySelectedCourse)}
                  />
                </div>
              )}

            </div>
          </div>
        </section>
      </main>
    </>
  );
}

// Add these helper functions before the closing of the SearchPage component
// Helper functions for color coding
const getScoreColor = (score: number) => {
  if (!score) return "text-gray-500";
  if (score >= 4) return "text-green-600";
  if (score >= 3) return "text-yellow-600";
  return "text-red-600";
};

const getDifficultyColor = (difficulty: number) => {
  if (!difficulty) return "text-gray-500";
  if (difficulty >= 4) return "text-red-600";
  if (difficulty >= 3) return "text-yellow-600";
  return "text-green-600";
};
