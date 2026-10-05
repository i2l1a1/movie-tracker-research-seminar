import type { ReactNode } from 'react'

type Props = {
    open: boolean
    title: string
    children: ReactNode
    onClose: () => void
}

export function Modal({ open, title, children, onClose }: Props) {
    if (!open) {
        return null
    }

    return (
        <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/70 p-4 sm:items-center">
            <button
                type="button"
                aria-label="Close dialog backdrop"
                className="absolute inset-0 cursor-default"
                onClick={onClose}
            />
            <div className="relative z-10 w-full max-w-lg rounded-xl border border-line bg-panel p-5 shadow-2xl sm:p-6">
                <div className="mb-4 flex items-start justify-between gap-3">
                    <h2 className="font-display text-xl font-semibold text-cream">{title}</h2>
                    <button
                        type="button"
                        onClick={onClose}
                        className="rounded-md px-2 py-1 text-muted transition hover:bg-panel-hover hover:text-cream"
                    >
                        Close
                    </button>
                </div>
                {children}
            </div>
        </div>
    )
}
