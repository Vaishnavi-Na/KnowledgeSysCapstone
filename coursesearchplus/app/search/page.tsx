/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import Link from "next/link";
import NavbarElse from "@/components/navbarElse";
import { useEffect, useState } from "react";

const server_endpoint = "http://localhost:8000";

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
    <button
      className={`${baseClasses} ${colorClasses}`}
      onClick={onCourseClick}
    >
      {buttonText}
    </button>
  );
}

export default function SearchPage() {
  const [remainingGroups, setRemainingGroups] = useState<string[][]>([]);
  const [mainSelectedCourse, setMainSelectedCourse] = useState<string | null>(
    null
  ); // Main selected course
  const [mainPrereqStructure, setMainPrereqStructure] = useState<string[][]>(
    []
  ); // Main prereq struc
  const [secondarySelectedCourse, setSecondarySelectedCourse] = useState<
    string | null
  >(null); // Secondary selected course
  const [secondaryPrereqStructure, setSecondaryPrereqStructure] = useState<
    string[][]
  >([]); // Secondary prereq struc
  const [page, setPage] = useState(0);
  const groupsPerPage = 6;
  const maxPage = Math.ceil(remainingGroups.length / groupsPerPage);
  const pagedGroups = remainingGroups.slice(
    page * groupsPerPage,
    (page + 1) * groupsPerPage
  );
  const [searchInput, setSearchInput] = useState("");

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
          // console.log('Received from get_remain API:', data);
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
        setMainSelectedCourse(course);
        // console.log('Received from calc_remain API:', data);
        setMainPrereqStructure(data);
        // Reset secondary course selected
        setSecondarySelectedCourse(null);
        setSecondaryPrereqStructure([]);
      });
  };

  const handleSecondaryCourseClick = (course: string) => {
    const transcript = JSON.parse(localStorage.getItem("transcript") || "{}");
    const query = new URLSearchParams({ course }).toString();

    fetch(`http://127.0.0.1:8000/courses/calc_remain?${query}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(transcript),
    })
      .then((res) => res.json())
      .then((data) => {
        setSecondarySelectedCourse(course);
        setSecondaryPrereqStructure(data);
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
              Find the perfect courses based on your preferences. Search by
              course number, professor name, or keywords to discover detailed
              information about classes at Ohio State University.
            </p>

            {/* Search Input */}
            <div className="flex gap-4">
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder="Search courses..."
                className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-red-500"
              />
              <button className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition-colors">
                Search
              </button>
            </div>
          </section>
        </div>

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
                  onClick={() => setPage((p) => Math.max(p - 1, 0))}
                >
                  ◀ Prev
                </button>
                <span className="text-gray-700">
                  Page {page + 1} / {maxPage}
                </span>
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
                    <div
                      key={colIndex}
                      className="flex flex-col items-center bg-white p-2 rounded shadow min-w-[120px]"
                    >
                      <span className="text-xs text-gray-500 mb-1">
                        AND Group {colIndex + 1}
                      </span>
                      {orGroup.map((course) => (
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
                <p className="text-gray-500 italic">
                  Click a course to view prerequisites.
                </p>
              )}

              {/* Secondary selected course panel */}
              {secondarySelectedCourse && (
                <div className="mt-8">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold mb-2">
                      Prerequisites for {secondarySelectedCourse}
                    </h3>
                    {secondaryPrereqStructure.length !== 0 && (
                      <SendToSearchButton
                        buttonText="Send to Search"
                        onCourseClick={() =>
                          setSearchInput(secondarySelectedCourse)
                        }
                        variant="blue"
                      />
                    )}
                  </div>
                  <div className="overflow-x-auto">
                    <div className="flex gap-4">
                      {secondaryPrereqStructure.map((orGroup, colIndex) => (
                        <div
                          key={colIndex}
                          className="flex flex-col items-center bg-white p-2 rounded shadow min-w-[120px]"
                        >
                          <span className="text-xs text-gray-500 mb-1">
                            AND Group {colIndex + 1}
                          </span>
                          {orGroup.map((course) => (
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
                    buttonText={"Ready to Take: " + mainSelectedCourse}
                    onCourseClick={() => setSearchInput(mainSelectedCourse)}
                  />
                </div>
              )}
              {secondarySelectedCourse &&
                secondaryPrereqStructure.length === 0 && (
                  <div className="mt-4">
                    <SendToSearchButton
                      buttonText={"Ready to Take: " + secondarySelectedCourse}
                      onCourseClick={() =>
                        setSearchInput(secondarySelectedCourse)
                      }
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
