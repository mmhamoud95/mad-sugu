import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const storedUser = browser ? localStorage.getItem('user') : null;
const storedToken = browser ? localStorage.getItem('token') : null;

export const user = writable(storedUser ? JSON.parse(storedUser) : null);
export const token = writable(storedToken);

export function login(userData, tokenData) {
	user.set(userData);
	token.set(tokenData);
	if (browser) {
		localStorage.setItem('user', JSON.stringify(userData));
		localStorage.setItem('token', tokenData);
	}
}

export function logout() {
	user.set(null);
	token.set(null);
	if (browser) {
		localStorage.removeItem('user');
		localStorage.removeItem('token');
	}
}
