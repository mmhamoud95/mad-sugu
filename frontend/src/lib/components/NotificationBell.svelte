<script>
	import { onMount } from 'svelte';
	import { notifications, unreadCount, fetchNotifications, markAsRead } from '$lib/stores/notifications';
	
	let showDropdown = false;
	
	onMount(() => {
		fetchNotifications();
		// Poll for new notifications every 30 seconds
		const interval = setInterval(fetchNotifications, 30000);
		return () => clearInterval(interval);
	});
	
	function toggleDropdown() {
		showDropdown = !showDropdown;
	}
	
	async function handleNotificationClick(notification) {
		await markAsRead(notification.id);
		// Navigate to the related content if available
		if (notification.annonce_id) {
			window.location.href = `/annonces/${notification.annonce_id}`;
		}
	}
	
	function getNotificationIcon(type) {
		const icons = {
			'new_message': '💬',
			'new_favorite': '❤️',
			'annonce_sold': '✅',
			'annonce_expired': '⏰',
			'alert_matched': '🔔',
			'new_review': '⭐',
			'boost_expired': '📢',
			'admin_message': '👮'
		};
		return icons[type] || '🔔';
	}
	
	function formatTime(dateString) {
		const date = new Date(dateString);
		const now = new Date();
		const diff = now - date;
		const minutes = Math.floor(diff / 60000);
		const hours = Math.floor(diff / 3600000);
		const days = Math.floor(diff / 86400000);
		
		if (minutes < 1) return 'À l\'instant';
		if (minutes < 60) return `Il y a ${minutes} min`;
		if (hours < 24) return `Il y a ${hours} h`;
		return `Il y a ${days} j`;
	}
</script>

<div class="relative">
	<button
		on:click={toggleDropdown}
		class="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none"
		aria-label="Notifications"
	>
		<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
		</svg>
		{#if $unreadCount > 0}
			<span class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
				{$unreadCount}
			</span>
		{/if}
	</button>
	
	{#if showDropdown}
		<div class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
			<div class="p-4 border-b border-gray-200">
				<h3 class="text-lg font-semibold">Notifications</h3>
			</div>
			
			{#if $notifications.length === 0}
				<div class="p-4 text-center text-gray-500">
					Aucune notification
				</div>
			{:else}
				<div class="divide-y divide-gray-200">
					{#each $notifications as notification}
						<button
							on:click={() => handleNotificationClick(notification)}
							class="w-full p-4 text-left hover:bg-gray-50 transition-colors {notification.is_read ? 'opacity-60' : 'bg-blue-50'}"
						>
							<div class="flex items-start space-x-3">
								<span class="text-2xl">{getNotificationIcon(notification.type)}</span>
								<div class="flex-1 min-w-0">
									<p class="text-sm font-medium text-gray-900">
										{notification.title}
									</p>
									<p class="text-sm text-gray-600 mt-1">
										{notification.message}
									</p>
									<p class="text-xs text-gray-400 mt-1">
										{formatTime(notification.created_at)}
									</p>
								</div>
								{#if !notification.is_read}
									<div class="w-2 h-2 bg-blue-600 rounded-full"></div>
								{/if}
							</div>
						</button>
					{/each}
				</div>
			{/if}
		</div>
	{/if}
</div>

<!-- Click outside to close -->
{#if showDropdown}
	<button
		on:click={() => showDropdown = false}
		class="fixed inset-0 z-40"
		aria-label="Close notifications"
	></button>
{/if}
