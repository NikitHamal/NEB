const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:4000/api';

type TokenProvider = () => Promise<string | null>;

class ApiClient {
    private baseUrl: string;
    private tokenProvider?: TokenProvider;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    setTokenProvider(provider: TokenProvider) {
        this.tokenProvider = provider;
    }

    private async getHeaders(includeAuth: boolean = true): Promise<Headers> {
        const headers = new Headers();
        headers.append('Content-Type', 'application/json');
        if (includeAuth) {
            const token = await this.tokenProvider?.();
            if (token) {
                headers.append('Authorization', `Bearer ${token}`);
            }
        }

        return headers;
    }

    private async handleResponse<T>(response: Response): Promise<T> {
        const result: unknown = await response.json().catch(() => null);

        if (!response.ok) {
            const body = result as Record<string, unknown> | null;
            const message =
                typeof body?.error === 'string'
                    ? body.error
                    : typeof body?.message === 'string'
                      ? body.message
                      : null;
            const error = new Error(message || 'API request failed') as Error & { status?: number };
            error.status = response.status;
            throw error;
        }

        return result as T;
    }

    async get<T>(endpoint: string, includeAuth: boolean = true): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'GET',
            headers: await this.getHeaders(includeAuth),
        });

        return this.handleResponse(response);
    }

    async post<T>(endpoint: string, body?: unknown, includeAuth: boolean = true): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: await this.getHeaders(includeAuth),
            body: body ? JSON.stringify(body) : undefined,
        });

        return this.handleResponse(response);
    }

    async patch<T>(endpoint: string, body?: unknown, includeAuth: boolean = true): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'PATCH',
            headers: await this.getHeaders(includeAuth),
            body: body ? JSON.stringify(body) : undefined,
        });

        return this.handleResponse(response);
    }

    async put<T>(endpoint: string, body?: unknown, includeAuth: boolean = true): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'PUT',
            headers: await this.getHeaders(includeAuth),
            body: body ? JSON.stringify(body) : undefined,
        });

        return this.handleResponse(response);
    }

    async delete<T>(endpoint: string, includeAuth: boolean = true): Promise<T> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'DELETE',
            headers: await this.getHeaders(includeAuth),
        });

        return this.handleResponse(response);
    }

    async postForm<T>(endpoint: string, body: FormData, includeAuth: boolean = true): Promise<T> {
        const headers = new Headers();
        if (includeAuth) {
            const token = await this.tokenProvider?.();
            if (token) {
                headers.append('Authorization', `Bearer ${token}`);
            }
        }
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers,
            body,
        });
        return this.handleResponse(response);
    }
}

export const apiClient = new ApiClient(API_BASE_URL);
