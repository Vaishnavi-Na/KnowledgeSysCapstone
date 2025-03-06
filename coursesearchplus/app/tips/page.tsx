'use client';

import NavbarElse from '@/components/navbarElse';

export default function SchedulingTips() {
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold text-[#bb0000] mb-6">Scheduling Tips</h1>

          {/* Scheduling Tips Section */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold text-[#bb0000] mb-4">General Tips</h2>
            <ul className="list-disc pl-6 text-lg">
              <li>Schedule classes with people you know.</li>
              <li>Get priority scheduling if possible.</li>
              <li>Create and update your four-year plan.</li>
              <li>Use a curriculum sheet to track progress.</li>
              <li>Avoid overloading your schedule—challenge yourself, but be mindful of your best learning times.</li>
              <li>Keep a spreadsheet of classes you have credit for and those you need.</li>
              <li>Consider scheduling ECE 2360 instead of ECE 2020 for an easier CSE-focused alternative.</li>
              <li>Utilize OSU CSE Same Day Express for quick scheduling help.</li>
            </ul>
          </section>

          {/* Curriculum Sheet Image */}
          <section className="flex justify-center mt-6">
            <img src="/bingosheet.png" alt="Sample Curriculum Sheet" className="rounded-lg shadow-md max-w-full h-auto" />
          </section>

          {/* Prerequisite Images */}
          <section className="flex justify-center mt-6 space-x-4">
            <img src="/prereq1.png" alt="CSE Core Prerequisite Chart" className="rounded-lg shadow-md w-1/3 h-auto" />
            <img src="/prereq2.png" alt="CSE Capstone Prerequisite Chart" className="rounded-lg shadow-md w-1/3 h-auto" />
          </section>


          {/* Minor and Electives Section */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left mt-6">
            <h2 className="text-2xl font-semibold text-[#bb0000] mb-4">Complete a Minor & Earn Non-CSE Technical Electives</h2>
            <p className="text-lg">A minor can help you gain additional knowledge while fulfilling 7-8 credit hours of non-CSE technical electives. Some options include:</p>
            <ul className="list-disc pl-6 text-lg mt-4 grid grid-cols-2 gap-2">
              <li>Air Science</li>
              <li>Astronomy & Astrophysics</li>
              <li>Biochemistry</li>
              <li>Biology</li>
              <li>Biomedical Engineering</li>
              <li>Business</li>
              <li>Business Analytics</li>
              <li>Cognitive Science</li>
              <li>Computational Science & Engineering</li>
              <li>Economics</li>
              <li>Entrepreneurship & Innovation</li>
              <li>Forensic Science</li>
              <li>Game Studies</li>
              <li>Geographic Information Science</li>
              <li>Math</li>
              <li>Microbiology</li>
              <li>Neuroscience</li>
              <li>Physics</li>
              <li>Professional Writing</li>
              <li>Psychology</li>
              <li>Security & Intelligence</li>
              <li>Statistics</li>
            </ul>
          </section>

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
