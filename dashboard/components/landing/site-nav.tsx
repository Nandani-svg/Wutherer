import Link from "next/link";
import { BrandMark } from "@/components/landing/brand-mark";

export function SiteNav() {
  return (
    <header className="outer-nav outer-nav-classic">
      <Link href="/" className="brand-lockup" aria-label="Wutherer home">
        <span className="brand-mark brand-mark-circle">
          <BrandMark />
        </span>
        <span className="brand-word">Wutherer</span>
      </Link>

      <nav className="nav-classic" aria-label="Primary">
        <Link href="/dashboard">Dashboard</Link>
      </nav>
    </header>
  );
}
