import { api } from './client';

export async function getFavorites() {
	return api.get('/favorites');
}

export async function addFavorite(annonceId) {
	return api.post(`/favorites/${annonceId}`, {});
}

export async function removeFavorite(annonceId) {
	return api.delete(`/favorites/${annonceId}`);
}

export async function checkFavorite(annonceId) {
	return api.get(`/favorites/check/${annonceId}`);
}
