import { apiRequest } from './client'
import type {
    Movie,
    MovieCreate,
    MovieListParams,
    MovieStats,
} from '../types/movie'

function toQuery(params: MovieListParams & { limit?: number }): string {
    const search = new URLSearchParams()
    if (params.status) {
        search.set('status', params.status)
    }
    if (params.type) {
        search.set('type', params.type)
    }
    if (params.q) {
        search.set('q', params.q)
    }
    if (params.limit != null) {
        search.set('limit', String(params.limit))
    }
    const query = search.toString()
    return query ? `?${query}` : ''
}

export const movieApi = {
    list(params: MovieListParams = {}): Promise<Movie[]> {
        return apiRequest<Movie[]>(`/movies${toQuery(params)}`)
    },

    create(payload: MovieCreate): Promise<Movie> {
        return apiRequest<Movie>('/movies', {
            method: 'POST',
            body: JSON.stringify(payload),
        })
    },

    update(id: number, payload: MovieCreate): Promise<Movie> {
        return apiRequest<Movie>(`/movies/${id}`, {
            method: 'PATCH',
            body: JSON.stringify(payload),
        })
    },

    remove(id: number): Promise<void> {
        return apiRequest<void>(`/movies/${id}`, { method: 'DELETE' })
    },

    stats(): Promise<MovieStats> {
        return apiRequest<MovieStats>('/movies/stats')
    },

    upcoming(params: MovieListParams & { limit?: number } = {}): Promise<Movie[]> {
        return apiRequest<Movie[]>(`/movies/upcoming${toQuery(params)}`)
    },
}
