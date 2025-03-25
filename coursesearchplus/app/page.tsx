'use client';

import React from 'react';
import Link from 'next/link';
import NavbarHome from '@/components/navbarHome';
import { motion } from 'framer-motion';

export default function Home() {
  // Animation variants for staggered animations
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3
      }
    }
  };
  
  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <>
      <NavbarHome />
      <main className="flex min-h-screen flex-col items-center justify-center p-6 md:p-24 bg-gradient-to-b from-white to-gray-100">
        <motion.div 
          className="z-10 max-w-5xl w-full font-mono"
          initial="hidden"
          animate="show"
          variants={container}
        >
          {/* Hero Section */}
          <motion.div className="mb-16 text-center md:text-left" variants={item}>
            <motion.h1 
              className="text-4xl md:text-6xl font-bold mb-4 text-red-600"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              Plan the right courses,
              <span className="block md:text-right">
                with the right professor.
              </span>
            </motion.h1>
            <motion.p 
              className="text-xl md:text-2xl text-gray-700"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 1 }}
            >
              Find and manage your courses easily with Course Search Plus!
            </motion.p>
          </motion.div>

          {/* Features Section */}
          <motion.div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16" variants={item}>
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
              whileHover={{ y: -5 }}
            >
              <div className="text-red-500 text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-2">Upload Transcript</h3>
              <p className="text-gray-600">Upload your OSU transcript and let us help you plan your remaining semesters based on your completed courses.</p>
            </motion.div>
            
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
              whileHover={{ y: -5 }}
            >
              <div className="text-red-500 text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-2">Search Courses</h3>
              <p className="text-gray-600">Find courses with detailed information including professor ratings and class times that fit your schedule.</p>
            </motion.div>
            
            <motion.div 
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
              whileHover={{ y: -5 }}
            >
              <div className="text-red-500 text-4xl mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-2">Build Schedule</h3>
              <p className="text-gray-600">Create your perfect four-year plan, considering your specialization, co-ops, and preferred professors.</p>
            </motion.div>
          </motion.div>

          {/* Call to Action */}
          <motion.div 
            className="text-center"
            variants={item}
            whileHover={{ scale: 1.05 }}
          >
            <Link 
              href="/about" 
              className="inline-block px-8 py-4 bg-red-600 text-white font-bold rounded-full hover:bg-red-700 transition-colors shadow-md"
            >
              Learn More →
            </Link>
          </motion.div>
        </motion.div>
      </main>
    </>
  );
}