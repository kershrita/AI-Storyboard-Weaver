import ReactMarkdown from "react-markdown";
import blogContent from "../blogpost/capstone_blogpost.md?raw";

export default function About() {
  return (
    <section className="p-8 max-w-4xl mx-auto">
      <h2 className="text-3xl font-orbitron text-cinematic-gold mb-6">About AI Storyboard Weaver</h2>
      <div className="prose text-soft-white font-montserrat">
        <ReactMarkdown>{blogContent}</ReactMarkdown>
      </div>
    </section>
  );
}