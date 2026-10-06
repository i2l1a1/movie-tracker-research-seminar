import { useEffect, useState, type FormEvent } from 'react'
import type { Movie } from '../types/movie'
import {
    emptyMovieForm,
    toMovieCreate,
    validateMovieForm,
    type MovieFormErrors,
    type MovieFormValues,
} from '../lib/movieForm'
import { Modal } from './Modal'

type Props = {
    open: boolean
    movie: Movie | null
    submitting: boolean
    error: string | null
    onClose: () => void
    onSubmit: (values: ReturnType<typeof toMovieCreate>) => Promise<void>
}

function fromMovie(movie: Movie): MovieFormValues {
    return {
        title: movie.title,
        type: movie.type,
        status: movie.status,
        rating: movie.rating == null ? '' : String(movie.rating),
        next_release_date: movie.next_release_date ?? '',
    }
}

export function MovieFormModal({
    open,
    movie,
    submitting,
    error,
    onClose,
    onSubmit,
}: Props) {
    const [values, setValues] = useState<MovieFormValues>(emptyMovieForm())
    const [errors, setErrors] = useState<MovieFormErrors>({})

    useEffect(() => {
        if (!open) {
            return
        }
        setValues(movie ? fromMovie(movie) : emptyMovieForm())
        setErrors({})
    }, [open, movie])

    function updateField<K extends keyof MovieFormValues>(
        key: K,
        value: MovieFormValues[K],
    ) {
        setValues((current) => {
            const next = { ...current, [key]: value }
            if (key === 'status' && value === 'planned') {
                next.rating = ''
            }
            return next
        })
    }

    async function handleSubmit(event: FormEvent) {
        event.preventDefault()
        const nextErrors = validateMovieForm(values)
        setErrors(nextErrors)
        if (Object.keys(nextErrors).length > 0) {
            return
        }
        await onSubmit(toMovieCreate(values))
    }

    return (
        <Modal
            open={open}
            title={movie ? 'Edit film or series' : 'Add film or series'}
            onClose={onClose}
        >
            <form className="space-y-3 text-left" onSubmit={handleSubmit}>
                <label className="block text-sm">
                    <span className="mb-1 block text-muted">Title</span>
                    <input
                        value={values.title}
                        onChange={(event) => updateField('title', event.target.value)}
                        className="w-full rounded-lg border border-line bg-stage px-3 py-2 text-cream outline-none ring-gold/40 focus:ring-2"
                    />
                    {errors.title ? (
                        <span className="mt-1 block text-xs text-danger">{errors.title}</span>
                    ) : null}
                </label>

                <div className="grid gap-3 sm:grid-cols-2">
                    <label className="block text-sm">
                        <span className="mb-1 block text-muted">Type</span>
                        <select
                            value={values.type}
                            onChange={(event) =>
                                updateField('type', event.target.value as MovieFormValues['type'])
                            }
                            className="w-full rounded-lg border border-line bg-stage px-3 py-2 text-cream outline-none ring-gold/40 focus:ring-2"
                        >
                            <option value="movie">Movie</option>
                            <option value="series">Series</option>
                        </select>
                    </label>
                    <label className="block text-sm">
                        <span className="mb-1 block text-muted">Status</span>
                        <select
                            value={values.status}
                            onChange={(event) =>
                                updateField(
                                    'status',
                                    event.target.value as MovieFormValues['status'],
                                )
                            }
                            className="w-full rounded-lg border border-line bg-stage px-3 py-2 text-cream outline-none ring-gold/40 focus:ring-2"
                        >
                            <option value="planned">Planned</option>
                            <option value="watched">Watched</option>
                        </select>
                    </label>
                </div>

                <label className="block text-sm">
                    <span className="mb-1 block text-muted">Rating (1–10)</span>
                    <input
                        type="number"
                        min={1}
                        max={10}
                        value={values.rating}
                        disabled={values.status !== 'watched'}
                        onChange={(event) => updateField('rating', event.target.value)}
                        className="w-full rounded-lg border border-line bg-stage px-3 py-2 text-cream outline-none ring-gold/40 focus:ring-2 disabled:opacity-50"
                    />
                    {errors.rating ? (
                        <span className="mt-1 block text-xs text-danger">{errors.rating}</span>
                    ) : null}
                </label>

                <label className="block text-sm">
                    <span className="mb-1 block text-muted">Next release date</span>
                    <input
                        type="date"
                        value={values.next_release_date}
                        onChange={(event) =>
                            updateField('next_release_date', event.target.value)
                        }
                        className="w-full rounded-lg border border-line bg-stage px-3 py-2 text-cream outline-none ring-gold/40 focus:ring-2"
                    />
                    {errors.next_release_date ? (
                        <span className="mt-1 block text-xs text-danger">
                            {errors.next_release_date}
                        </span>
                    ) : null}
                </label>

                {error ? (
                    <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
                        {error}
                    </p>
                ) : null}

                <div className="flex justify-end gap-2 pt-2">
                    <button
                        type="button"
                        onClick={onClose}
                        className="rounded-lg border border-line px-4 py-2 text-sm text-cream transition hover:bg-panel-hover"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={submitting}
                        className="rounded-lg bg-gold px-4 py-2 text-sm font-medium text-ink transition hover:bg-gold-soft disabled:opacity-60"
                    >
                        {submitting ? 'Saving…' : 'Save'}
                    </button>
                </div>
            </form>
        </Modal>
    )
}
