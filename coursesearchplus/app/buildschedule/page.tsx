"use client";

import NavbarElse from "@/components/navbarElse";
import curriculum from "@/app/buildschedule/curriculum.json"; // Import curriculum JSON directly
import { useEffect, useState } from "react";

const server_endpoint = "http://localhost:8000";

export default function BuildSchedulePage() {
  const [schedule, setSchedule] = useState<string[][]>([]);
  useEffect(() => {
    const transcript = JSON.parse(localStorage.getItem("transcript") || "{}");
    const query = new URLSearchParams({ hours: "17" });

    if (transcript) {
      fetch(`${server_endpoint}/courses/gen_schedule?${query}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(transcript),
      })
        .then((res) => res.json())
        .then((data) => {
          setSchedule(data);
        });
    }
  }, []);

  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold text-[#bb0000] mb-6">
            Build Your Schedule
          </h1>

          {/* Description Section */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold text-[#bb0000] mb-4">
              Schedule Builder
            </h2>
            <p className="text-lg leading-relaxed">
              Welcome to the Schedule Builder! Here you can create your perfect
              course schedule based on your preferences and requirements. We'll
              help you find the best professors and class times that work for
              you.
            </p>
          </section>

          {schedule.length > 0 && (
            <section className="mt-12 text-left w-full">
              <h2 className="text-2xl font-semibold text-[#bb0000] mb-6 text-center">
                Generated Schedule
              </h2>
              <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {schedule.map((semester, index) => (
                  <div
                    key={index}
                    className="bg-white border border-gray-300 rounded-2xl shadow-md p-6"
                  >
                    <h3 className="text-xl font-bold text-[#4d4d4d] mb-4">
                      Semester {index + 1}
                    </h3>
                    <ul className="list-disc list-inside space-y-2 text-gray-800 text-lg">
                      {semester.map((course, courseIndex) => (
                        <li key={courseIndex}>{course}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Curriculum Table */}
          <div className="max-w-5xl mx-auto mt-12 p-6">
            <h2 className="text-3xl font-bold text-[#bb0000] text-center mb-6">
              {curriculum.degree}
            </h2>
            <h3 className="text-2xl font-semibold text-[#4d4d4d] text-center mb-4">
              {curriculum.specialization}
            </h3>

            {Object.entries(curriculum.categories).map(
              ([category, courses]) => (
                <div key={category} className="mb-12">
                  <div className="bg-[#bb0000] text-white font-bold text-xl p-3 rounded-lg text-center shadow-md">
                    {category}
                  </div>
                  <table className="w-full border-collapse border border-gray-300 mt-4">
                    <thead>
                      <tr className="bg-[#d3d3d3] text-[#333] text-lg">
                        <th className="border border-gray-300 px-4 py-3 text-left">
                          Course
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left">
                          Title
                        </th>
                        <th className="border border-gray-300 px-4 py-3 text-left">
                          Credit Hours
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {courses.map((course, index) => (
                        <tr
                          key={index}
                          className="border border-gray-300 text-lg"
                        >
                          <td className="border border-gray-300 px-4 py-2">
                            {course.course || "-"}
                          </td>
                          <td className="border border-gray-300 px-4 py-2">
                            {course.title || course.category}
                          </td>
                          <td className="border border-gray-300 px-4 py-2">
                            {course.hours ?? "-"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )
            )}
          </div>

          {/* Legend Section */}
          <div className="bg-gray-100 p-8 rounded-lg shadow-md mt-12 max-w-xxl text-left">
            <h3 className="text-xl font-semibold text-[#bb0000] mb-4">
              Legend
            </h3>
            <ul className="list-disc pl-6 text-lg">
              <li>
                <strong className="text-black-700">
                  General Education Requirements:
                </strong>{" "}
                24 credit hours
              </li>
              <li>
                <strong className="text-black-700">
                  College/Degree Requirements:
                </strong>{" "}
                20 credit hours
              </li>
              <li>
                <strong className="text-black-700">Major Core:</strong> 42-45
                credit hours
              </li>
              <li>
                <strong className="text-black-700">
                  Required Non-Major Courses:
                </strong>{" "}
                23 credit hours
              </li>
              <li>
                <strong className="text-black-700">
                  Technical/Directed/Targeted Electives; Career Courses:
                </strong>{" "}
                17 credit hours
              </li>
            </ul>
            <p className="mt-4 font-bold text-lg text-[#bb0000]">
              Minimum Total Credit Hours: 126
            </p>
          </div>
        </div>
      </main>
    </>
  );
}
