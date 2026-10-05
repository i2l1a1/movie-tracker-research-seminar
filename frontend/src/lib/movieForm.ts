import type { MovieCreate, MovieStatus } from '../types/movie'

export type MovieFormValues = {
    title: string
    type: 'movie' | 'series'
    status: MovieStatus
    rating: string
    next_release_date: string
}

export type MovieFormErrors = Partial<Record<keyof MovieFormValues, string>>

export function emptyMovieForm(): MovieFormValues {
    return {
        title: '',
        type: 'movie',
        status: 'planned',
        rating: '',
        next_release_date: '',
    }
}

export function validateMovieForm(values: MovieFormValues): MovieFormErrors {
    const errors: MovieFormErrors = {}
    const title = values.title.trim()

    if (!title) {
        errors.title = 'Title is required'
    } else if (title.length > 255) {
        errors.title = 'Title must be at most 255 characters'
    }

    if (values.status === 'watched') {
        if (values.rating !== '') {
            const rating = Number(values.rating)
            if (!Number.isInteger(rating) || rating < 1 || rating > 10) {
                errors.rating = 'Rating must be an integer from 1 to 10'
            }
        }
    } else if (values.rating !== '') {
        errors.rating = 'Rating is only allowed when status is watched'
    }

    if (values.next_release_date) {
        if (!/^\d{4}-\d{2}-\d{2}$/.test(values.next_release_date)) {
            errors.next_release_date = 'Use date format YYYY-MM-DD'
        }
    }

    return errors
}

export function toMovieCreate(values: MovieFormValues): MovieCreate {
    const payload: MovieCreate = {
        title: values.title.trim(),
        type: values.type,
        status: values.status,
    }

    if (values.status === 'watched' && values.rating !== '') {
        payload.rating = Number(values.rating)
    } else {
        payload.rating = null
    }

    payload.next_release_date = values.next_release_date
        ? values.next_release_date
        : null

    return payload
}
