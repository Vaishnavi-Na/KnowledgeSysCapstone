'use client';

import React from 'react';
import Link from 'next/link';
import NavbarHome from '@/components/navbarHome';

export default function Home() {
  return (
    <>
      <NavbarHome />
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
          <h1 className="text-4xl font-bold mb-4">
            CourseSearchPlus
          </h1>
          <p className="text-xl mb-8">
            Find and manage your courses easily
          </p>
          <Link 
            href="/about" 
            className="text-foreground hover:underline"
          >
            About Us →
          </Link>
        </div>
      </main>
    </>
  );
}