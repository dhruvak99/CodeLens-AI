import { Card } from "@/components/ui/card";
import { features } from "@/features/landing/data";
import { MotionDiv, MotionSection } from "@/features/landing/motion";

export function FeaturesSection() {
  return (
    <MotionSection
      className="px-4 py-20 sm:px-6 lg:px-8"
      id="features"
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-120px" }}
      transition={{ duration: 0.55 }}
    >
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 max-w-2xl">
          <p className="mb-3 text-sm font-medium text-secondary">Features</p>
          <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Built for Python understanding and SQL fluency.
          </h2>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <MotionDiv
              initial={{ opacity: 0, y: 18 }}
              key={feature.title}
              transition={{ duration: 0.45, delay: index * 0.05 }}
              viewport={{ once: true }}
              whileInView={{ opacity: 1, y: 0 }}
            >
              <Card className="h-full p-6 transition duration-300 hover:-translate-y-1 hover:border-white/[0.16] hover:bg-card">
                <div className="mb-5 grid size-11 place-items-center rounded-xl border border-white/[0.08] bg-white/[0.04] text-primary">
                  <feature.icon className="size-5" />
                </div>
                <h3 className="text-lg font-semibold text-white">
                  {feature.title}
                </h3>
                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {feature.description}
                </p>
              </Card>
            </MotionDiv>
          ))}
        </div>
      </div>
    </MotionSection>
  );
}
