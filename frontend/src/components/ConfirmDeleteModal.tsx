import type { Movie } from '../types/movie'
import { Modal } from './Modal'

type Props = {
    open: boolean
    movie: Movie | null
    submitting: boolean
    error: string | null
    onClose: () => void
    onConfirm: () => Promise<void>
}

export function ConfirmDeleteModal({
    open,
    movie,
    submitting,
    error,
    onClose,
    onConfirm,
}: Props) {
    return (
        <Modal open={open} title="Delete title" onClose={onClose}>
            <p className="text-left text-sm text-muted">
                Delete <span className="font-medium text-cream">{movie?.title}</span>? This
                cannot be undone.
            </p>
            {error ? (
                <p className="mt-3 rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
                    {error}
                </p>
            ) : null}
            <div className="mt-5 flex justify-end gap-2">
                <button
                    type="button"
                    onClick={onClose}
                    className="rounded-lg border border-line px-4 py-2 text-sm text-cream transition hover:bg-panel-hover"
                >
                    Cancel
                </button>
                <button
                    type="button"
                    disabled={submitting}
                    onClick={() => {
                        void onConfirm()
                    }}
                    className="rounded-lg bg-danger px-4 py-2 text-sm font-medium text-cream transition hover:brightness-110 disabled:opacity-60"
                >
                    {submitting ? 'Deleting…' : 'Delete'}
                </button>
            </div>
        </Modal>
    )
}
