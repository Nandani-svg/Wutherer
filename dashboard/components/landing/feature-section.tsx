"use client";

import { useEffect, useRef } from "react";
import { BarChart3, ShieldCheck, Terminal } from "lucide-react";

const features = [
  {
    icon: ShieldCheck,
    title: "Safety that stays legible",
    text: "Review moderation cases, adjust message filters, set verification, and access anti-nuke controls.",
  },
  {
    icon: Terminal,
    title: "Useful automation",
    text: "Build custom commands and response triggers instead of relying on a generic configuration maze.",
  },
  {
    icon: BarChart3,
    title: "Context when it matters",
    text: "Use server analytics, backup inventory, and integrations to inform the next change.",
  },
];

export function FeatureSection() {
    const gridRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const grid = gridRef.current;
        if (!grid) return;
        const cards = Array.from(grid.querySelectorAll<HTMLElement>(".feature-card"));
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            grid.classList.add("feat-js");
            cards.forEach((card) => card.classList.add("is-visible"));
            return;
        }
        grid.classList.add("feat-js");
        const io = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        (entry.target as HTMLElement).classList.add("is-visible");
                        io.unobserve(entry.target);
                    }
                });
            },
            {threshold: 0.2}
        );
        cards.forEach((card) => io.observe(card));
        return () => io.disconnect();
    }, []);

    const onMove = (event: React.MouseEvent<HTMLElement>) => {
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        if (window.matchMedia("(hover: none)").matches) return;
        const el = event.currentTarget;
        const rect = el.getBoundingClientRect();
        el.style.setProperty("--mx", ((event.clientX - rect.left) / rect.width).toFixed(3));
        el.style.setProperty("--my", ((event.clientY - rect.top) / rect.height).toFixed(3));
    };

    return (
        <section id="capabilities" className="section-wrap" style={{ paddingBottom: 64 }}>
            <p className="section-kicker">Built around real jobs</p>
            <h2 className="section-title">A control center, not a wall of tiles</h2>
            <p className="section-copy">
                Each module uses the data Wutherer already manages. Open a server, see the available controls, and make focused changes with clear feedback.
            </p>
            <div className="feature-grid" ref={gridRef}>
                {features.map((feature, index) => {
                    const Icon = feature.icon;
                    return (
                        <article
                        key={feature.title}
                        className="feature-card"
                        style={{ "--rd": `${index * 110}ms `} as React.CSSProperties}
                        onMouseMove={onMove}
                        >
                            <div className="feature-icon">
                                <Icon size={18} aria-hidden="true" />
                            </div>
                            <h3 style={{ marginTop: 16, fontSize: 16, fontWeight: 500}}>{feature.title}</h3>
                            <p style={{ marginTop: 8, color: "#9bb0bc", fontSize: 14, lineHeight: 1.65 }}>{feature.text}</p>
                        </article>
                    );
                })}
            </div>
        </section>
    );
}