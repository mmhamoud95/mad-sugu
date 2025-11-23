import { api } from './client';

export async function getAnnonces(params = {}) {
	const queryString = new URLSearchParams(params).toString();
	return api.get(`/annonces${queryString ? '?' + queryString : ''}`);
}

export async function getAnnonce(id) {
	return api.get(`/annonces/${id}`);
}

export async function createAnnonce(data) {
	return api.post('/annonces', data);
}

export async function updateAnnonce(id, data) {
	return api.put(`/annonces/${id}`, data);
}

export async function deleteAnnonce(id) {
	return api.delete(`/annonces/${id}`);
}

export async function uploadAnnonceImages(id, files) {
	const formData = new FormData();
	for (const file of files) {
		formData.append('images', file);
	}
	return api.postForm(`/annonces/${id}/images`, formData);
}
