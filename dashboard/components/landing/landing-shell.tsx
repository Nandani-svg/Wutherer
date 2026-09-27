"use client";

import { Hero } from "@/components/landing/hero";
import { SiteNav } from "@/components/landing/site-nav";

export function LandingShell() {
    return (
        <>
        <SiteNav />
        <div className="landing-pad">
            <section id="product" className="landing-stage">
                <Hero />
            </section>
        </div>
        </>
    );
}