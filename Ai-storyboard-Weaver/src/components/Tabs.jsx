export default function Tabs({ activeTab, setActiveTab }) {
    const tabs = ["demo", "gallery", "about"];
    return (
      <div className="flex justify-center space-x-4 mb-8">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-2 rounded-xl transition shadow-md font-semibold ${
              activeTab === tab
                ? "bg-[#00D4FF] text-[#1C2526]"
                : "bg-[#2E3A40] hover:bg-[#3C4B50] text-[#F5F5F5]"
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>
    );
  }