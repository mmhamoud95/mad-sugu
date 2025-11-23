<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import AnnonceCard from '$lib/components/AnnonceCard.svelte';
	import { api } from '$lib/api/client';
	
	let annonces = [];
	let loading = true;
	let error = null;
	
	// Filters
	let search = '';
	let category_id = null;
	let city = '';
	let min_price = '';
	let max_price = '';
	
	$: queryParams = $page.url.searchParams;
	
	onMount(async () => {
		// Get filters from URL
		search = queryParams.get('q') || '';
		category_id = queryParams.get('category') || null;
		city = queryParams.get('city') || '';
		
		await loadAnnonces();
	});
	
	async function loadAnnonces() {
		loading = true;
		error = null;
		
		try {
			// Build query params
			const params = new URLSearchParams();
			if (search) params.append('search', search);
			if (category_id) params.append('category_id', category_id);
			if (city) params.append('city', city);
			if (min_price) params.append('min_price', min_price);
			if (max_price) params.append('max_price', max_price);
			params.append('limit', '24');
			
			annonces = await api.get(`/annonces?${params.toString()}`);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}
	
	function handleFilterSubmit() {
		loadAnnonces();
	}
</script>

<svelte:head>
	<title>Annonces - MadSugu</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold mb-4">Toutes les annonces</h1>
		
		<!-- Filters -->
		<div class="card mb-6">
			<form on:submit|preventDefault={handleFilterSubmit} class="space-y-4">
				<div class="grid grid-cols-1 md:grid-cols-4 gap-4">
					<div>
						<label for="search" class="block text-sm font-medium text-gray-700 mb-1">
							Recherche
						</label>
						<input
							id="search"
							type="text"
							bind:value={search}
							placeholder="Mots-clés..."
							class="input"
						/>
					</div>
					
					<div>
						<label for="city" class="block text-sm font-medium text-gray-700 mb-1">
							Ville
						</label>
						<input
							id="city"
							type="text"
							bind:value={city}
							placeholder="Ex: Dakar"
							class="input"
						/>
					</div>
					
					<div>
						<label for="min_price" class="block text-sm font-medium text-gray-700 mb-1">
							Prix min
						</label>
						<input
							id="min_price"
							type="number"
							bind:value={min_price}
							placeholder="0"
							class="input"
						/>
					</div>
					
					<div>
						<label for="max_price" class="block text-sm font-medium text-gray-700 mb-1">
							Prix max
						</label>
						<input
							id="max_price"
							type="number"
							bind:value={max_price}
							placeholder="Illimité"
							class="input"
						/>
					</div>
				</div>
				
				<div class="flex justify-end">
					<button type="submit" class="btn-primary">
						Rechercher
					</button>
				</div>
			</form>
		</div>
	</div>
	
	<!-- Results -->
	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
		</div>
	{:else if error}
		<div class="text-center py-12">
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg inline-block">
				Erreur: {error}
			</div>
		</div>
	{:else if annonces.length > 0}
		<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
			{#each annonces as annonce}
				<AnnonceCard {annonce} />
			{/each}
		</div>
	{:else}
		<div class="text-center py-12 text-gray-600">
			<p class="text-lg">Aucune annonce trouvée</p>
			<p class="mt-2">Essayez de modifier vos critères de recherche</p>
		</div>
	{/if}
</div>
