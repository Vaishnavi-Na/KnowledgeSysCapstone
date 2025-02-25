// app/api/upload/route.ts

import fs from 'fs';
import { NextResponse } from 'next/server';
import path from 'path';
import { ChildProcess, spawn } from 'child_process';

export async function POST(req: Request) {
  const formData = await req.formData();
  const file = formData.get('file') as File;

  if (!file) {
    return new NextResponse(
      JSON.stringify({ message: 'No file uploaded' }),
      { status: 400 }
    );
  }
  // Make sure the uploaded file is a pdf
  if (file.type !== 'application/pdf') {
    return new NextResponse(
        JSON.stringify({ message: 'File is not a pdf' }),
        { status: 400 }
      );
  }

  try {
    // Binary version of the pdf
    const fileBuffer = Buffer.from(await file.arrayBuffer());

    // Create a thread that runs the advising report scraper
    const advRepScraperPath = path.join(process.cwd(), 'adv_rep_scraper/scraper_json.py');
    var pythonThread = null;
    if (process.platform === "linux") {
      pythonThread = spawn('python3', [advRepScraperPath]);
    }
    else if (process.platform === "darwin"){
      pythonThread = spawn('python3', [advRepScraperPath]);
    }
    else {
      pythonThread = spawn('python', [advRepScraperPath]);
    }
    pythonThread.stdin.write(fileBuffer);
    pythonThread.stdin.end();

    // Collect the Python script's output
    var result = '';
    for await (const data of pythonThread.stdout) {
      result += data;
    }

    // Return transcript
    // Transcript has two values, special (string) and courses (set)
    const transcript = JSON.parse(result);
    return NextResponse.json(transcript, {status: 200});
  }
  catch(error) {
    console.error('Error scraping transcript:', error);
    return new NextResponse(
      JSON.stringify({
        message: 'Error uploading file',
      }),
      { status: 500 }
    );
  }
}
