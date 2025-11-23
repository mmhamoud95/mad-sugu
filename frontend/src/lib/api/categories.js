import { api } from './client';

export async function getCategories() {
	return api.get('/categories');
}

export async function getCategory(id) {
	return api.get(`/categories/${id}`);
}

export async function createCategory(data) {
	return api.post('/categories', data);
}

export async function updateCategory(id, data) {
	return api.put(`/categories/${id}`, data);
}

export async function deleteCategory(id) {
	return api.delete(`/categories/${id}`);
}
