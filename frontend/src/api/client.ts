const API_BASE = '/api'

function formatDetail(details: unknown): string {
    if (typeof details === 'string') {
        return details
    }
    if (details && typeof details === 'object' && 'detail' in details) {
        const detail = (details as { detail: unknown }).detail
        if (typeof detail === 'string') {
            return detail
        }
        if (Array.isArray(detail)) {
            return detail
                .map((item) => {
                    if (item && typeof item === 'object' && 'msg' in item) {
                        return String((item as { msg: unknown }).msg)
                    }
                    return String(item)
                })
                .join('. ')
        }
    }
    return 'Request failed'
}

export async function apiRequest<T>(
    path: string,
    init?: RequestInit,
): Promise<T> {
    const response = await fetch(`${API_BASE}${path}`, {
        headers: {
            'Content-Type': 'application/json',
            ...(init?.headers ?? {}),
        },
        ...init,
    })

    if (response.status === 204) {
        return undefined as T
    }

    const payload = await response.json().catch(() => null)

    if (!response.ok) {
        throw new Error(formatDetail(payload))
    }

    return payload as T
}
