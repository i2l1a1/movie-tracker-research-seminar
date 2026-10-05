import type { MovieStats } from '../types/movie'

type Props = {
    stats: MovieStats | null
    loading: boolean
}

export function StatsBar({ stats, loading }: Props) {
    const items = [
        { label: 'Total', value: stats?.total },
        { label: 'Watched', value: stats?.watched },
        { label: 'Planned', value: stats?.planned },
        { label: 'Movies', value: stats?.movies },
        { label: 'Series', value: stats?.series },
        {
            label: 'Avg rating',
            value: stats?.average_rating == null ? '—' : stats.average_rating.toFixed(1),
        },
    ]

    return (
        <section className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
            {items.map((item) => (
                <div
                    key={item.label}
                    className="rounded-xl border border-line bg-panel px-3 py-3"
                >
                    <p className="text-xs uppercase tracking-wide text-muted">{item.label}</p>
                    <p className="mt-1 text-xl font-semibold text-gold-soft">
                        {loading ? '…' : (item.value ?? '—')}
                    </p>
                </div>
            ))}
        </section>
    )
}
