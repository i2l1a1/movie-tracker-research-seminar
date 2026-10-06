import { useEffect, useState } from 'react'
import { movieApi } from '../api/movies'
import { ConfirmDeleteModal } from '../components/ConfirmDeleteModal'
import { ListTabs } from '../components/ListTabs'
import { MovieFormModal } from '../components/MovieFormModal'
import { MovieList } from '../components/MovieList'
import { StatsBar } from '../components/StatsBar'
import { Toolbar } from '../components/Toolbar'
import { errorMessage } from '../lib/errorMessage'
import type { ListTab } from '../types/listTab'
import type { Movie, MovieCreate, MovieStats, MovieStatus, MovieType } from '../types/movie'

export function WatchlistPage() {
    const [q, setQ] = useState('')
    const [status, setStatus] = useState<'' | MovieStatus>('')
    const [type, setType] = useState<'' | MovieType>('')
    const [tab, setTab] = useState<ListTab>('all')
    const [reload, setReload] = useState(0)

    const [movies, setMovies] = useState<Movie[]>([])
    const [stats, setStats] = useState<MovieStats | null>(null)
    const [listLoading, setListLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const [formOpen, setFormOpen] = useState(false)
    const [editing, setEditing] = useState<Movie | null>(null)
    const [formSubmitting, setFormSubmitting] = useState(false)
    const [formError, setFormError] = useState<string | null>(null)

    const [deleting, setDeleting] = useState<Movie | null>(null)
    const [deleteSubmitting, setDeleteSubmitting] = useState(false)
    const [deleteError, setDeleteError] = useState<string | null>(null)

    useEffect(() => {
        let cancelled = false
        setListLoading(true)
        setError(null)

        const params = {
            q: q.trim() || undefined,
            status: status || undefined,
            type: type || undefined,
        }

        const request =
            tab === 'all'
                ? movieApi.list(params)
                : movieApi.upcoming({ ...params, limit: 100 })

        void request
            .then((items) => {
                if (!cancelled) {
                    setMovies(items)
                }
            })
            .catch((err: unknown) => {
                if (!cancelled) {
                    setError(errorMessage(err))
                }
            })
            .finally(() => {
                if (!cancelled) {
                    setListLoading(false)
                }
            })

        return () => {
            cancelled = true
        }
    }, [q, status, type, tab, reload])

    useEffect(() => {
        let cancelled = false

        void movieApi
            .stats()
            .then((nextStats) => {
                if (!cancelled) {
                    setStats(nextStats)
                }
            })
            .catch((err: unknown) => {
                if (!cancelled) {
                    setError(errorMessage(err))
                }
            })

        return () => {
            cancelled = true
        }
    }, [reload])

    async function saveMovie(payload: MovieCreate) {
        setFormSubmitting(true)
        setFormError(null)
        try {
            if (editing) {
                await movieApi.update(editing.id, payload)
            } else {
                await movieApi.create(payload)
            }
            setFormOpen(false)
            setEditing(null)
            setReload((value) => value + 1)
        } catch (err) {
            setFormError(errorMessage(err))
        } finally {
            setFormSubmitting(false)
        }
    }

    async function confirmDelete() {
        if (!deleting) {
            return
        }
        setDeleteSubmitting(true)
        setDeleteError(null)
        try {
            await movieApi.remove(deleting.id)
            setDeleting(null)
            setReload((value) => value + 1)
        } catch (err) {
            setDeleteError(errorMessage(err))
        } finally {
            setDeleteSubmitting(false)
        }
    }

    return (
        <div className="mx-auto min-h-svh w-full max-w-6xl px-4 py-8 sm:px-6">
            <header className="mb-8 flex flex-col gap-4 text-left sm:flex-row sm:items-center sm:justify-between">
                <h1 className="font-display text-3xl font-semibold text-cream sm:text-4xl">
                    My watchlist
                </h1>
                <button
                    type="button"
                    onClick={() => {
                        setEditing(null)
                        setFormError(null)
                        setFormOpen(true)
                    }}
                    className="shrink-0 rounded-lg bg-gold px-4 py-2.5 font-medium text-ink transition hover:bg-gold-soft"
                >
                    Add movie or series
                </button>
            </header>

            <div className="space-y-5">
                <StatsBar stats={stats} loading={stats === null} />

                <Toolbar
                    q={q}
                    status={status}
                    type={type}
                    onQChange={setQ}
                    onStatusChange={setStatus}
                    onTypeChange={setType}
                />

                {error ? (
                    <div className="rounded-xl border border-danger/40 bg-danger/10 px-4 py-3 text-left text-sm text-danger">
                        {error}
                    </div>
                ) : null}

                <ListTabs value={tab} onChange={setTab} />

                <MovieList
                    movies={movies}
                    loading={listLoading}
                    emptyMessage={
                        tab === 'all' ? undefined : 'No upcoming release dates yet.'
                    }
                    onEdit={(movie) => {
                        setEditing(movie)
                        setFormError(null)
                        setFormOpen(true)
                    }}
                    onDelete={(movie) => {
                        setDeleting(movie)
                        setDeleteError(null)
                    }}
                />
            </div>

            <MovieFormModal
                open={formOpen}
                movie={editing}
                submitting={formSubmitting}
                error={formError}
                onClose={() => {
                    if (!formSubmitting) {
                        setFormOpen(false)
                        setEditing(null)
                    }
                }}
                onSubmit={saveMovie}
            />

            <ConfirmDeleteModal
                open={deleting !== null}
                movie={deleting}
                submitting={deleteSubmitting}
                error={deleteError}
                onClose={() => {
                    if (!deleteSubmitting) {
                        setDeleting(null)
                    }
                }}
                onConfirm={confirmDelete}
            />
        </div>
    )
}
