import { get } from 'svelte/store';
import { token } from '$lib/stores/auth';

const API_BASE_URL = '/api/v1';

async function request(endpoint, options = {}) {
	const authToken = get(token);
	
	const headers = {
		'Content-Type': 'application/json',
		...options.headers
	};
	
	if (authToken) {
		headers['Authorization'] = `Bearer ${authToken}`;
	}
	
	const config = {
		...options,
		headers
	};
	
	const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
	
	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
		throw new Error(error.detail || 'An error occurred');
	}
	
	// Handle 204 No Content
	if (response.status === 204) {
		return null;
	}
	
	return response.json();
}

export const api = {
	get: (endpoint) => request(endpoint, { method: 'GET' }),
	post: (endpoint, data) => request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
	put: (endpoint, data) => request(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
	delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
	
	// Multipart form data (for file uploads)
	postForm: async (endpoint, formData) => {
		const authToken = get(token);
		const headers = {};
		
		if (authToken) {
			headers['Authorization'] = `Bearer ${authToken}`;
		}
		
		const response = await fetch(`${API_BASE_URL}${endpoint}`, {
			method: 'POST',
			headers,
			body: formData
		});
		
		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
			throw new Error(error.detail || 'An error occurred');
		}
		
		return response.json();
	}
};
