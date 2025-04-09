const galleryItems = [
    { title: "Detective in 1920s Chicago", image: "/images/storyboard1.png" },
  ];
  
  export default function Gallery() {
    return (
      <section className="p-8 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {galleryItems.map((item) => (
          <div
            key={item.title}
            className="bg-[#F5F5F5] p-4 rounded-lg shadow-md transition-transform duration-300 hover:scale-105"
          >
            <img src={item.image} alt={item.title} className="w-full h-48 object-cover rounded" />
            <h3 className="mt-2 text-lg font-orbitron text-[#1C2526]">{item.title}</h3>
          </div>
        ))}
      </section>
    );
  }