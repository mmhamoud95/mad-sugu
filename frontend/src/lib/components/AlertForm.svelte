<script>
	import { onMount } from 'svelte';
	
	export let onSubmit = null;
	
	let title = '';
	let keywords = '';
	let categoryId = null;
	let locationCity = '';
	let minPrice = null;
	let maxPrice = null;
	let frequency = 'instant';
	
	let categories = [];
	let loading = false;
	let error = null;
	let success = false;
	
	onMount(async () => {
		await fetchCategories();
	});
	
	async function fetchCategories() {
		try {
			const response = await fetch('http://localhost:8000/api/v1/categories/');
			if (response.ok) {
				categories = await response.json();
			}
		} catch (err) {
			console.error('Failed to fetch categories:', err);
		}
	}
	
	async function handleSubmit() {
		loading = true;
		error = null;
		success = false;
		
		try {
			const token = localStorage.getItem('token');
			if (!token) {
				error = 'Vous devez être connecté';
				return;
			}
			
			const response = await fetch('http://localhost:8000/api/v1/alerts/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					title,
					keywords: keywords || null,
					category_id: categoryId || null,
					location_city: locationCity || null,
					min_price: minPrice || null,
					max_price: maxPrice || null,
					frequency
				})
			});
			
			if (response.ok) {
				success = true;
				// Reset form
				title = '';
				keywords = '';
				categoryId = null;
				locationCity = '';
				minPrice = null;
				maxPrice = null;
				frequency = 'instant';
				
				if (onSubmit) onSubmit();
			} else {
				const data = await response.json();
				error = data.detail || 'Erreur lors de la création de l\'alerte';
			}
		} catch (err) {
			error = 'Erreur de connexion';
			console.error(err);
		} finally {
			loading = false;
		}
	}
</script>

<div class="bg-white rounded-lg shadow-md p-6">
	<h3 class="text-xl font-semibold mb-4">Créer une alerte</h3>
	
	{#if success}
		<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
			Alerte créée avec succès !
		</div>
	{/if}
	
	{#if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
			{error}
		</div>
	{/if}
	
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<!-- Title -->
		<div>
			<label for="title" class="block text-sm font-medium text-gray-700 mb-1">
				Nom de l'alerte *
			</label>
			<input
				type="text"
				id="title"
				bind:value={title}
				required
				maxlength="100"
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
				placeholder="Ex: iPhone 13 à Dakar"
			/>
		</div>
		
		<!-- Keywords -->
		<div>
			<label for="keywords" class="block text-sm font-medium text-gray-700 mb-1">
				Mots-clés (séparés par des espaces)
			</label>
			<input
				type="text"
				id="keywords"
				bind:value={keywords}
				maxlength="500"
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
				placeholder="Ex: iphone 13 pro max"
			/>
		</div>
		
		<!-- Category -->
		<div>
			<label for="category" class="block text-sm font-medium text-gray-700 mb-1">
				Catégorie
			</label>
			<select
				id="category"
				bind:value={categoryId}
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
			>
				<option value={null}>Toutes les catégories</option>
				{#each categories as category}
					<option value={category.id}>
						{category.icon} {category.name}
					</option>
				{/each}
			</select>
		</div>
		
		<!-- Location -->
		<div>
			<label for="city" class="block text-sm font-medium text-gray-700 mb-1">
				Ville
			</label>
			<input
				type="text"
				id="city"
				bind:value={locationCity}
				maxlength="100"
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
				placeholder="Ex: Dakar"
			/>
		</div>
		
		<!-- Price range -->
		<div class="grid grid-cols-2 gap-4">
			<div>
				<label for="minPrice" class="block text-sm font-medium text-gray-700 mb-1">
					Prix minimum (FCFA)
				</label>
				<input
					type="number"
					id="minPrice"
					bind:value={minPrice}
					min="0"
					step="1000"
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
					placeholder="0"
				/>
			</div>
			<div>
				<label for="maxPrice" class="block text-sm font-medium text-gray-700 mb-1">
					Prix maximum (FCFA)
				</label>
				<input
					type="number"
					id="maxPrice"
					bind:value={maxPrice}
					min="0"
					step="1000"
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
					placeholder="Illimité"
				/>
			</div>
		</div>
		
		<!-- Frequency -->
		<div>
			<label for="frequency" class="block text-sm font-medium text-gray-700 mb-1">
				Fréquence des notifications
			</label>
			<select
				id="frequency"
				bind:value={frequency}
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
			>
				<option value="instant">Instantané</option>
				<option value="daily">Quotidien</option>
				<option value="weekly">Hebdomadaire</option>
			</select>
		</div>
		
		<!-- Submit button -->
		<button
			type="submit"
			disabled={loading}
			class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
		>
			{loading ? 'Création en cours...' : 'Créer l\'alerte'}
		</button>
	</form>
</div>
