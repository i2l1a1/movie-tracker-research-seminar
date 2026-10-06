import type { MovieStatus, MovieType } from '../types/movie'

type Props = {
    q: string
    status: '' | MovieStatus
    type: '' | MovieType
    onQChange: (value: string) => void
    onStatusChange: (value: '' | MovieStatus) => void
    onTypeChange: (value: '' | MovieType) => void
}

export function Toolbar({
    q,
    status,
    type,
    onQChange,
    onStatusChange,
    onTypeChange,
}: Props) {
    return (
        <section className="rounded-xl border border-line bg-panel p-4">
            <div className="grid gap-3 sm:grid-cols-3">
                <label className="block text-left text-sm">
                    <span className="mb-1 block text-muted">Search</span>
                    <input
                        value={q}
                        onChange={(event) => onQChange(event.target.value)}
                        placeholder="Title"
                        className="box-border h-10 w-full rounded-lg border border-line bg-stage px-3 outline-none ring-gold/40 placeholder:text-muted/70 focus:ring-2"
                    />
                </label>
                <label className="block text-left text-sm">
                    <span className="mb-1 block text-muted">Status</span>
                    <select
                        value={status}
                        onChange={(event) => onStatusChange(event.target.value as '' | MovieStatus)}
                        className="box-border h-10 w-full rounded-lg border border-line bg-stage px-3 text-cream outline-none ring-gold/40 focus:ring-2"
                    >
                        <option value="">All</option>
                        <option value="watched">Watched</option>
                        <option value="planned">Planned</option>
                    </select>
                </label>
                <label className="block text-left text-sm">
                    <span className="mb-1 block text-muted">Type</span>
                    <select
                        value={type}
                        onChange={(event) => onTypeChange(event.target.value as '' | MovieType)}
                        className="box-border h-10 w-full rounded-lg border border-line bg-stage px-3 text-cream outline-none ring-gold/40 focus:ring-2"
                    >
                        <option value="">All</option>
                        <option value="movie">Movie</option>
                        <option value="series">Series</option>
                    </select>
                </label>
            </div>
        </section>
    )
}
