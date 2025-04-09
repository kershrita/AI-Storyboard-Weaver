export default function Demo() {
  return (
    <section className="p-8 max-w-4xl mx-auto">
      <div className="border-2 border-neon-blue p-6 rounded-lg bg-deep-space">
        <h2 className="text-2xl font-orbitron text-cinematic-gold mb-4">Input Plot</h2>
        <textarea
          className="w-full p-2 mb-4 bg-[#2E3A40] text-soft-white rounded"
          placeholder="Describe your story..."
          readOnly
          value="A detective discovers aliens in 1920s Chicago."
        />
        <button
          className="px-4 py-2 bg-neon-blue text-deep-space rounded hover:shadow-[0_0_10px_#00D4FF]"
          onClick={() => alert("This is a static demo. The model will be integrated later.")}
        >
          Generate
        </button>
        <div className="mt-6">
          <h2 className="text-2xl font-orbitron text-cinematic-gold">Generated Storyboard</h2>
          <p>Scene 1: The detective walks down a foggy street, hat tilted low.</p>
          <p>Scene 2: A glowing craft hovers above the speakeasy.</p>
          <img src="/images/demo1.png" alt="Demo Output" className="mt-4 w-full" />
        </div>
      </div>
    </section>
  );
}