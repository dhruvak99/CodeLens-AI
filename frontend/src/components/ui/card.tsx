import * as React from "react";

import { cn } from "@/lib/utils";

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-2xl border border-white/[0.08] bg-card/80 shadow-[0_18px_80px_rgba(0,0,0,0.28)] backdrop-blur",
      className
    )}
    {...props}
  />
));
Card.displayName = "Card";

export { Card };
