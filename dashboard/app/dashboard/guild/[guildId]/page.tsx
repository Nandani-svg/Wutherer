import Link from "next/link";

export default function GuildPage() {
	return (
		<section>
			<p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary-light">Server overview</p>
			<h1 className="mt-3 text-3xl font-semibold text-white">Your Discord server</h1>
			<p className="mt-2 text-sm text-slate-400">Select a module from the dashboard navigation to configure it.</p>
			<Link href="./analytics" className="mt-8 inline-flex rounded-md border border-card-border px-4 py-3 text-sm text-white hover:bg-surface-hover">View analytics</Link>
		</section>
	);
}
