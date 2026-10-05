import type { Movie } from '../types/movie'

type Props = {
    movies: Movie[]
    loading: boolean
    emptyMessage?: string
    onEdit: (movie: Movie) => void
    onDelete: (movie: Movie) => void
}

export function MovieList({
    movies,
    loading,
    emptyMessage = 'No titles match the current filters.',
    onEdit,
    onDelete,
}: Props) {
    if (loading) {
        return (
            <div className="rounded-xl border border-line bg-panel px-4 py-10 text-center text-muted">
                Loading collection…
            </div>
        )
    }

    if (movies.length === 0) {
        return (
            <div className="rounded-xl border border-line bg-panel px-4 py-10 text-center text-muted">
                {emptyMessage}
            </div>
        )
    }

    return (
        <ul className="space-y-3">
            {movies.map((movie) => (
                <li
                    key={movie.id}
                    className="rounded-xl border border-line bg-panel p-4 transition hover:bg-panel-hover"
                >
                    <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                        <div className="text-left">
                            <h3 className="text-lg font-semibold text-cream">{movie.title}</h3>
                            <p className="mt-1 text-sm text-muted">
                                {movie.type} · {movie.status}
                                {movie.rating != null ? ` · ${movie.rating}/10` : ''}
                                {movie.next_release_date
                                    ? ` · next: ${movie.next_release_date}`
                                    : ''}
                            </p>
                        </div>
                        <div className="flex gap-2">
                            <button
                                type="button"
                                onClick={() => onEdit(movie)}
                                className="rounded-lg border border-line px-3 py-1.5 text-sm text-cream transition hover:border-gold hover:text-gold-soft"
                            >
                                Edit
                            </button>
                            <button
                                type="button"
                                onClick={() => onDelete(movie)}
                                className="rounded-lg border border-danger/40 px-3 py-1.5 text-sm text-danger transition hover:bg-danger/10"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </li>
            ))}
        </ul>
    )
}
