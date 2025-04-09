import { useState } from "react";

export default function Demo() {
  const [plot, setPlot] = useState("");
  const [storyboard, setStoryboard] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      // Replace this with your actual API endpoint
      const response = await fetch("http://your-api-endpoint/generate-storyboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plot }),
      });
      const data = await response.json();
      setStoryboard(data);
    } catch (error) {
      console.error("Error generating storyboard:", error);
      setStoryboard({ error: "Failed to generate storyboard" });
    }
    setLoading(false);
  };

  return (
    <section className="p-8 max-w-4xl mx-auto">
      <div className="border-2 border-[#00D4FF] p-6 rounded-lg bg-[#1C2526]">
        <h2 className="text-2xl font-orbitron text-[#FFD700] mb-4">Input Plot</h2>
        <textarea
          className="w-full p-2 mb-4 bg-[#2E3A40] text-[#F5F5F5] rounded"
          value={plot}
          onChange={(e) => setPlot(e.target.value)}
          placeholder="Describe your story..."
        />
        <button
          onClick={handleGenerate}
          className="px-4 py-2 bg-[#00D4FF] text-[#1C2526] rounded hover:shadow-[0_0_10px_#00D4FF]"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate"}
        </button>
        {storyboard && (
          <div className="mt-6">
            <h2 className="text-2xl font-orbitron text-[#FFD700]">Generated Storyboard</h2>
            {storyboard.error ? (
              <p className="text-red-500">{storyboard.error}</p>
            ) : (
              <>
                <p>{storyboard.description || "Your storyboard content here"}</p>
                <img src="/images/demo1.png" alt="Demo Output" className="mt-4 w-full" />
              </>
            )}
          </div>
        )}
      </div>
    </section>
  );
}