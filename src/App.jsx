import { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Tabs from './components/Tabs';
import Demo from './components/Demo';
import Gallery from './components/Gallery';
import About from './components/About';
import Footer from './components/Footer';

function App() {
  const [activeTab, setActiveTab] = useState('demo');

  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-blue-900 text-soft-white">
      <Header />
      <Hero />
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
      {activeTab === 'demo' && <Demo />}
      {activeTab === 'gallery' && <Gallery />}
      {activeTab === 'about' && <About />}
      <Footer />
    </div>
  );
}

export default App;