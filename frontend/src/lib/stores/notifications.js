import { writable } from 'svelte/store';

export const notifications = writable([]);
export const unreadCount = writable(0);

export async function fetchNotifications() {
	try {
		const token = localStorage.getItem('token');
		if (!token) return;

		const response = await fetch('http://localhost:8000/api/v1/notifications/', {
			headers: {
				'Authorization': `Bearer ${token}`
			}
		});

		if (response.ok) {
			const data = await response.json();
			notifications.set(data);
			const unread = data.filter(n => !n.is_read).length;
			unreadCount.set(unread);
		}
	} catch (error) {
		console.error('Failed to fetch notifications:', error);
	}
}

export async function markAsRead(notificationId) {
	try {
		const token = localStorage.getItem('token');
		if (!token) return;

		const response = await fetch(`http://localhost:8000/api/v1/notifications/${notificationId}/read`, {
			method: 'PUT',
			headers: {
				'Authorization': `Bearer ${token}`
			}
		});

		if (response.ok) {
			await fetchNotifications();
		}
	} catch (error) {
		console.error('Failed to mark notification as read:', error);
	}
}

export async function markAllAsRead() {
	try {
		const token = localStorage.getItem('token');
		if (!token) return;

		const response = await fetch('http://localhost:8000/api/v1/notifications/mark-all-read', {
			method: 'PUT',
			headers: {
				'Authorization': `Bearer ${token}`
			}
		});

		if (response.ok) {
			await fetchNotifications();
		}
	} catch (error) {
		console.error('Failed to mark all notifications as read:', error);
	}
}
