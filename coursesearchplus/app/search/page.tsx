/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import Link from "next/link";
import NavbarElse from "@/components/navbarElse";
import { useEffect, useState } from "react";

const server_endpoint = "http://localhost:8000";

export default function SearchPage() {
  const [remainingGroups, setRemainingGroups] = useState<string[][]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string | null>(null);
  const [prereqStructure, setPrereqStructure] = useState<string[][]>([]);
  const [page, setPage] = useState(0);
  const groupsPerPage = 6;

  useEffect(() => {
    const transcript = localStorage.getItem("transcript");
    if (transcript) {
      const parsed = JSON.parse(transcript);
      fetch(`${server_endpoint}/courses/get_remain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("Received from get_remain API:", data);
          setRemainingGroups(data.remaining_groups);
        });
    }
  }, []);

  const handleCourseClick = (course: string) => {
    const transcript = JSON.parse(localStorage.getItem("transcript") || "{}");
    const query = new URLSearchParams({ course }).toString();

    fetch(`${server_endpoint}/courses/calc_remain?${query}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(transcript),
    })
      .then((res) => res.json())
      .then((data) => {
        setSelectedCourse(course);
        console.log("Received from calc_remain API:", data);
        setPrereqStructure(data);
      });
  };

  const maxPage = Math.ceil(remainingGroups.length / groupsPerPage);

  const pagedGroups = remainingGroups.slice(
    page * groupsPerPage,
    (page + 1) * groupsPerPage
  );

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
              Find the perfect courses based on your preferences. Search by
              course number, professor name, or keywords to discover detailed
              information about classes at Ohio State University.
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

          {/* --- Requirement Group Panel --- */}
          <section className="flex w-full gap-6 mt-8">
            {/* Left: Requirement Groups */}
            <div className="w-3/5">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-semibold">Courses You Can Take</h2>
                <div className="space-x-2">
                  <button
                    className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                    disabled={page === 0}
                    onClick={() => setPage((p) => Math.max(p - 1, 0))}
                  >
                    ◀ Prev
                  </button>
                  <button
                    className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
                    disabled={page >= maxPage - 1}
                    onClick={() => setPage((p) => Math.min(p + 1, maxPage - 1))}
                  >
                    Next ▶
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {pagedGroups.map((group, idx) => (
                  <div
                    key={idx}
                    className="border rounded-lg p-4 shadow bg-white"
                  >
                    <h3 className="font-bold mb-2">
                      Requirement Group {page * groupsPerPage + idx + 1}
                    </h3>
                    <div className="flex gap-3 flex-wrap">
                      {group.map((course) => (
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
              <h2 className="text-xl font-semibold mb-3">
                Course Prerequisites
              </h2>
              {selectedCourse ? (
                <>
                  <h3 className="text-lg font-bold mb-2">{selectedCourse}</h3>
                  <div className="flex gap-4 overflow-x-auto">
                    {prereqStructure.map((orGroup, colIndex) => (
                      <div
                        key={colIndex}
                        className="flex flex-col items-center bg-white p-2 rounded shadow min-w-[120px]"
                      >
                        <span className="text-xs text-gray-500 mb-1">
                          AND Group {colIndex + 1}
                        </span>
                        {orGroup.map((course) => (
                          <span
                            key={course}
                            className="bg-red-100 text-red-800 px-2 py-1 rounded mb-1 text-xs text-center"
                          >
                            {course}
                          </span>
                        ))}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p className="text-gray-500 italic">
                  Click a course to view prerequisites.
                </p>
              )}
            </div>
          </section>

          {/* Removed Back to Home Link */}
        </div>
      </main>
    </>
  );
}
