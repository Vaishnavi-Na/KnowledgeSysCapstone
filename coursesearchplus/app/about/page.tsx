import Link from 'next/link';

export default function AboutPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">
          About Page
        </h1>
        <p className="text-xl mb-8">
          Welcome to the About page of the app!
        </p>
        <Link 
          href="/" 
          className="text-foreground hover:underline"
        >
          ← Back to Home
        </Link>
      </div>
    </main>
  );
}
  