'use client';

import NavbarElse from '@/components/navbarElse';
import curriculum from '@/app/buildschedule/curriculum.json'; // Import curriculum JSON directly

export default function BuildSchedulePage() {
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold mb-6">Build Your Schedule</h1>

          {/* Description Section */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold mb-4">Schedule Builder</h2>
            <p className="text-lg leading-relaxed">
              Welcome to the Schedule Builder! Here you can create your perfect course schedule 
              based on your preferences and requirements. We'll help you find the best professors 
              and class times that work for you.
            </p>
          </section>

          {/* Curriculum Table */}
          <div className="max-w-5xl mx-auto mt-12 p-6">
            <h2 className="text-2xl font-bold text-center mb-6">{curriculum.degree}</h2>
            <h3 className="text-xl font-semibold text-center mb-4">{curriculum.specialization}</h3>
            <p className="text-center mb-6">Total Credit Hours: {curriculum.total_credit_hours}</p>

            {Object.entries(curriculum.categories).map(([category, courses]) => (
              <div key={category} className="mb-8">
                <h3 className="text-xl font-semibold mb-4 bg-gray-200 p-2 rounded">{category}</h3>
                <table className="w-full border-collapse border border-gray-300">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="border border-gray-300 px-4 py-2 text-left">Course</th>
                      <th className="border border-gray-300 px-4 py-2 text-left">Title</th>
                      <th className="border border-gray-300 px-4 py-2 text-left">Credit Hours</th>
                    </tr>
                  </thead>
                  <tbody>
                    {courses.map((course, index) => (
                      <tr key={index} className="border border-gray-300">
                        <td className="border border-gray-300 px-4 py-2">{course.course || '-'}</td>
                        <td className="border border-gray-300 px-4 py-2">{course.title || course.category}</td>
                        <td className="border border-gray-300 px-4 py-2">{course.hours ?? '-'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
          </div>

          {/* Back to Home Link */}
          <div className="mt-12">
            <a href="/" className="text-foreground hover:underline text-lg">
              ← Back to Home
            </a>
          </div>
        </div>
      </main>
    </>
  );
}
