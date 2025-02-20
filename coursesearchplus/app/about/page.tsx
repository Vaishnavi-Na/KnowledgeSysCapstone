import Link from 'next/link';
import Image from 'next/image';
import NavbarElse from '@/components/navbarElse';

export default function AboutPage() {
  return (
    <>
      <NavbarElse />
      <main className="flex min-h-screen flex-col items-center p-10">
        {/* Centered Header */}
        

        {/* Main Content */}
        <div className="max-w-5xl w-full text-center mt-12 font-mono text-sm">
          <h1 className="text-4xl font-bold mb-4">About Page</h1>
          <p className="text-xl mb-8">
            Welcome to the About page of the app!
          </p>

          {/* Project Description */}
          <section className="bg-gray-100 p-6 rounded-lg shadow-md text-left">
            <h2 className="text-2xl font-semibold mb-4">What is OSU Elasti-Course Search Plus (Stan Edition) (SCRUMPTIOUS)™?</h2>
            <p className="text-lg leading-relaxed">
              Through scraping Rate My Professor, publicly available SEI rating scores, and the OSU Course Search Website, this website will generate a four-year plan for the user, ensuring they have the best professors possible for their specialization.
            </p>
            <p className="text-lg leading-relaxed mt-4">
              This platform also considers the user's course preferences and any co-op semesters while generating the schedule. No more worries about having literally Severus Snape as your professor. Try OSU Elasti-Course Search Plus (Stan Edition) (SCRUMPTIOUS)™ today!
            </p>
          </section>

          {/* Creators Section */}
          <section className="mt-12 text-left">
            <h2 className="text-3xl font-bold mb-6 text-center">Meet the Team</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Individual Creators */}
              {[
                { name: "Bella London", email: "London.73@osu.edu" },
                { name: "Kaushik Jegath", email: "Jegath.1@osu.edu" },
                { name: "Sophia Li", email: "Li.12808@osu.edu" },
                { name: "Vaishnavi Nayak", email: "Nayak.109@osu.edu" },
                { name: "Haozhe (Howard) Li", email: "Li.12529@osu.edu" },
                { name: "Ziheng Zhang", email: "Zhang.13617@osu.edu" },
                { name: "Srijan Bijjam", email: "Bijjam.1@osu.edu" },
                { name: "Iryna Kryvyak", email: "Kryvyak.1@osu.edu" },
              ].map((person, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg shadow-md">
                  <h3 className="text-xl font-semibold">{person.name}</h3>
                  <p><strong>Email:</strong> {person.email}</p>
                </div>
              ))}
            </div>
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
