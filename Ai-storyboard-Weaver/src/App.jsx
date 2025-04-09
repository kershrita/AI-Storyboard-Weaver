import { useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Tabs from "./components/Tabs";
import Demo from "./components/Demo";
import Gallery from "./components/Gallery";
import About from "./components/About";
import Footer from "./components/Footer";

export default function App() {
  const [activeTab, setActiveTab] = useState("demo");

  return (
    <div className="bg-gradient-to-b from-[#0B0F12] to-[#1C2526] text-[#F5F5F5] min-h-screen font-montserrat">
      <Header />
      <Hero />
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="px-6 md:px-20">
        {activeTab === "demo" && <Demo />}
        {activeTab === "gallery" && <Gallery />}
        {activeTab === "about" && <About />}
      </main>
      <Footer />
    </div>
  );
}