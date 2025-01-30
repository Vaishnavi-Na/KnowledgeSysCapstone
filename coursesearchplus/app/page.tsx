'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <div className="flex items-center space-x-4">
          <Image 
            src="/logo.png" 
            alt="CourseSearchPlus Logo" 
            width={50} 
            height={50} 
            className="rounded-md"
          />
        
          <h1 className="text-4xl font-bold mb-4">
            CourseSearchPlus
          </h1>
        </div>
        <p className="text-xl mb-8">
          Plan the right classes. With the right professor.
        </p>
        <Link 
          href="/about" 
          className="text-foreground hover:underline"
        >
          About Us →
        </Link>
      </div>
    </main>
  );
}