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
          <h1 className="text-5xl font-bold mb-4 text-red-500">
            Plan the right courses,
            <span className="block text-right">
              with the right professor.
            </span>
          </h1>
          <p className="text-2xl mb-8 text-red-500">
            Find and manage your courses easily with Course Search Plus!
          </p>
          <Link 
            href="/about" 
            className="text-foreground hover:underline"
          >
            Learn More →
          </Link>
        </div>
      </main>
    </>
  );
}