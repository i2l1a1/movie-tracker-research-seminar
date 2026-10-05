export type MovieType = 'movie' | 'series'
export type MovieStatus = 'watched' | 'planned'

export type Movie = {
    id: number
    title: string
    type: MovieType
    status: MovieStatus
    rating: number | null
    next_release_date: string | null
    created_at: string
    updated_at: string
}

export type MovieCreate = {
    title: string
    type: MovieType
    status: MovieStatus
    rating?: number | null
    next_release_date?: string | null
}

export type MovieStats = {
    total: number
    watched: number
    planned: number
    movies: number
    series: number
    average_rating: number | null
}

export type MovieListParams = {
    status?: MovieStatus
    type?: MovieType
    q?: string
}
