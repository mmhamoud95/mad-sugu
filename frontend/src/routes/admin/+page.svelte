<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	
	let stats = null;
	let loading = true;
	let error = null;
	
	onMount(async () => {
		const token = localStorage.getItem('token');
		if (!token) {
			goto('/auth/login');
			return;
		}
		
		await fetchDashboardStats();
	});
	
	async function fetchDashboardStats() {
		loading = true;
		error = null;
		
		try {
			const token = localStorage.getItem('token');
			const response = await fetch('http://localhost:8000/api/v1/admin/stats/dashboard', {
				headers: {
					'Authorization': `Bearer ${token}`
				}
			});
			
			if (response.ok) {
				stats = await response.json();
			} else if (response.status === 403) {
				error = 'Accès refusé. Vous n\'avez pas les permissions administrateur.';
			} else {
				error = 'Erreur lors du chargement des statistiques';
			}
		} catch (err) {
			error = 'Erreur de connexion';
			console.error(err);
		} finally {
			loading = false;
		}
	}
	
	function formatNumber(num) {
		return new Intl.NumberFormat('fr-FR').format(num);
	}
</script>

<svelte:head>
	<title>Dashboard Administrateur - MadSugu</title>
</svelte:head>

<div class="container mx-auto px-4 py-6 md:py-8">
	<h1 class="text-2xl md:text-3xl font-bold mb-6 md:mb-8">Dashboard Administrateur</h1>
	
	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-sm md:text-base text-gray-600">Chargement des statistiques...</p>
		</div>
	{:else if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded text-sm md:text-base">
			{error}
		</div>
	{:else if stats}
		<!-- Overview Cards -->
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
			<!-- Total Users -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-500 text-xs md:text-sm mb-1">Utilisateurs</p>
						<p class="text-2xl md:text-3xl font-bold text-gray-900">{formatNumber(stats.total_users)}</p>
					</div>
					<div class="bg-blue-100 rounded-full p-2 md:p-3">
						<svg class="w-6 h-6 md:w-8 md:h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
						</svg>
					</div>
				</div>
				<div class="mt-2 text-xs md:text-sm text-green-600">
					+{formatNumber(stats.new_users_7d)} cette semaine
				</div>
			</div>
			
			<!-- Total Annonces -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-500 text-xs md:text-sm mb-1">Annonces</p>
						<p class="text-2xl md:text-3xl font-bold text-gray-900">{formatNumber(stats.total_annonces)}</p>
					</div>
					<div class="bg-green-100 rounded-full p-2 md:p-3">
						<svg class="w-6 h-6 md:w-8 md:h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
						</svg>
					</div>
				</div>
				<div class="mt-2 text-xs md:text-sm text-green-600">
					+{formatNumber(stats.new_annonces_7d)} cette semaine
				</div>
			</div>
			
			<!-- Active Annonces -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-500 text-xs md:text-sm mb-1">Annonces actives</p>
						<p class="text-2xl md:text-3xl font-bold text-gray-900">{formatNumber(stats.active_annonces)}</p>
					</div>
					<div class="bg-purple-100 rounded-full p-2 md:p-3">
						<svg class="w-6 h-6 md:w-8 md:h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
						</svg>
					</div>
				</div>
			</div>
			
			<!-- Pending Annonces -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-500 text-xs md:text-sm mb-1">En attente</p>
						<p class="text-2xl md:text-3xl font-bold text-gray-900">{formatNumber(stats.pending_annonces)}</p>
					</div>
					<div class="bg-yellow-100 rounded-full p-2 md:p-3">
						<svg class="w-6 h-6 md:w-8 md:h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
						</svg>
					</div>
				</div>
			</div>
		</div>
		
		<!-- Activity Sections -->
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 mb-6 md:mb-8">
			<!-- 7 Days Activity -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<h2 class="text-lg md:text-xl font-semibold mb-3 md:mb-4">Activité - 7 derniers jours</h2>
				<div class="space-y-2 md:space-y-3">
					<div class="flex justify-between items-center">
						<span class="text-sm md:text-base text-gray-600">Nouveaux utilisateurs</span>
						<span class="text-sm md:text-base font-semibold text-blue-600">{formatNumber(stats.new_users_7d)}</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-sm md:text-base text-gray-600">Nouvelles annonces</span>
						<span class="text-sm md:text-base font-semibold text-green-600">{formatNumber(stats.new_annonces_7d)}</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-sm md:text-base text-gray-600">Messages envoyés</span>
						<span class="text-sm md:text-base font-semibold text-purple-600">{formatNumber(stats.new_messages_7d)}</span>
					</div>
				</div>
			</div>
			
			<!-- 30 Days Activity -->
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<h2 class="text-lg md:text-xl font-semibold mb-3 md:mb-4">Activité - 30 derniers jours</h2>
				<div class="space-y-2 md:space-y-3">
					<div class="flex justify-between items-center">
						<span class="text-sm md:text-base text-gray-600">Nouveaux utilisateurs</span>
						<span class="text-sm md:text-base font-semibold text-blue-600">{formatNumber(stats.new_users_30d)}</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-sm md:text-base text-gray-600">Nouvelles annonces</span>
						<span class="text-sm md:text-base font-semibold text-green-600">{formatNumber(stats.new_annonces_30d)}</span>
					</div>
				</div>
			</div>
		</div>
		
		<!-- Quick Actions -->
		<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
			<h2 class="text-lg md:text-xl font-semibold mb-3 md:mb-4">Actions rapides</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
				<a
					href="/admin/users"
					class="flex items-center justify-between p-3 md:p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 transition-colors"
				>
					<span class="text-sm md:text-base font-medium">Gérer les utilisateurs</span>
					<svg class="w-4 h-4 md:w-5 md:h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
					</svg>
				</a>
				<a
					href="/admin/annonces"
					class="flex items-center justify-between p-3 md:p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 transition-colors"
				>
					<span class="text-sm md:text-base font-medium">Modérer les annonces</span>
					<svg class="w-4 h-4 md:w-5 md:h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
					</svg>
				</a>
				<a
					href="/admin/analytics"
					class="flex items-center justify-between p-3 md:p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 transition-colors"
				>
					<span class="text-sm md:text-base font-medium">Voir les analytics</span>
					<svg class="w-4 h-4 md:w-5 md:h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
					</svg>
				</a>
			</div>
		</div>
	{/if}
</div>
