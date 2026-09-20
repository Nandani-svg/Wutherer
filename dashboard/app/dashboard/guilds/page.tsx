import Link from "next/link";

export default function GuildsPage() {
	return (
		<main className="mx-auto max-w-5xl px-6 py-12">
			<p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary-light">Workspace</p>
			<h1 className="mt-3 text-3xl font-semibold text-white">Choose a server</h1>
			<p className="mt-2 text-sm text-slate-400">Open a server to manage its Wutherer settings.</p>
			<Link href="/dashboard/guild/demo" className="mt-8 inline-flex rounded-md border border-card-border px-4 py-3 text-sm text-white hover:bg-surface-hover">Demo server</Link>
		</main>
	);
}
