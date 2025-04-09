import { motion } from "framer-motion";
import { Typewriter } from "react-simple-typewriter";

export default function Hero() {
  return (
    <section className="py-16 text-center">
      <motion.img
        src="/images/clapperboard.png"
        alt="Clapperboard"
        className="mx-auto mb-4 w-24 h-24"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      />
      <motion.h1
        className="text-5xl font-orbitron text-[#00D4FF] mb-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        AI Storyboard Weaver
      </motion.h1>
      <p className="text-xl text-[#FFD700]">
        <Typewriter words={["Turn Your Ideas into Cinematic Magic"]} loop={true} />
      </p>
    </section>
  );
}