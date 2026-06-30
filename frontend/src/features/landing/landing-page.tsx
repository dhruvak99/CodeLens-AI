import { ArchitectureSection } from "@/features/landing/architecture-section";
import { DemoSection } from "@/features/landing/demo-section";
import { FeaturesSection } from "@/features/landing/features-section";
import { Footer } from "@/features/landing/footer";
import { Hero } from "@/features/landing/hero";
import { Navbar } from "@/features/landing/navbar";

export function LandingPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <Navbar />
      <Hero />
      <FeaturesSection />
      <ArchitectureSection />
      <DemoSection />
      <Footer />
    </main>
  );
}
