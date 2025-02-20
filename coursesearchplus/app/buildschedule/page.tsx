'use client';

import Link from 'next/link';
import NavbarElse from '@/components/navbarElse';

export default function BuildSchedulePage() {
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        {/* Main Content */}
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
