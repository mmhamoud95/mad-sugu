<script>
	import { onMount } from 'svelte';
	import AnnonceCard from '$lib/components/AnnonceCard.svelte';
	import { api } from '$lib/api/client';
	
	let annonces = [];
	let categories = [];
	let loading = true;
	let error = null;
	
	onMount(async () => {
		try {
			// Load annonces and categories
			const [annoncesData, categoriesData] = await Promise.all([
				api.get('/annonces?limit=12'),
				api.get('/categories')
			]);
			
			annonces = annoncesData;
			categories = categoriesData;
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>MadSugu - Petites Annonces en Afrique de l'Ouest</title>
	<meta name="description" content="Achetez et vendez facilement en Afrique de l'Ouest. Trouvez des voitures, immobilier, emploi, électronique et plus encore.">
</svelte:head>

<!-- Hero Section -->
<section class="bg-gradient-to-r from-primary to-secondary text-white py-12 md:py-16 lg:py-20">
	<div class="container mx-auto px-4 text-center">
		<h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-3 md:mb-4">
			Achetez et Vendez Facilement
		</h1>
		<p class="text-base sm:text-lg md:text-xl lg:text-2xl mb-6 md:mb-8">
			La plateforme de petites annonces en Afrique de l'Ouest
		</p>
		<div class="max-w-2xl mx-auto">
			<form action="/recherche" method="GET" class="flex flex-col sm:flex-row gap-2 sm:gap-0">
				<input 
					type="text" 
					name="q"
					placeholder="Que recherchez-vous ?"
					class="flex-1 px-4 sm:px-6 py-3 sm:py-4 rounded-lg sm:rounded-l-lg sm:rounded-r-none text-gray-900 focus:outline-none focus:ring-2 focus:ring-accent"
				/>
				<button type="submit" class="bg-accent hover:bg-accent/90 px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-l-none sm:rounded-r-lg font-semibold transition-colors">
					Rechercher
				</button>
			</form>
		</div>
	</div>
</section>

<!-- Categories -->
<section class="container mx-auto px-4 py-8 md:py-12">
	<h2 class="text-2xl md:text-3xl font-bold mb-6 md:mb-8">Parcourir par catégorie</h2>
	
	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
		</div>
	{:else if categories.length > 0}
		<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 md:gap-4">
			{#each categories as category}
				<a 
					href="/categories/{category.slug}"
					class="card hover:shadow-lg transition-shadow text-center py-4 px-2"
				>
					<div class="text-3xl md:text-4xl mb-2">{category.icon || '📦'}</div>
					<h3 class="font-semibold text-xs md:text-sm">{category.name}</h3>
				</a>
			{/each}
		</div>
	{/if}
</section>

<!-- Featured Annonces -->
<section class="bg-gray-100 py-8 md:py-12">
	<div class="container mx-auto px-4">
		<div class="flex justify-between items-center mb-6 md:mb-8">
			<h2 class="text-2xl md:text-3xl font-bold">Annonces récentes</h2>
			<a href="/annonces" class="text-sm md:text-base text-primary hover:underline">Voir tout</a>
		</div>
		
		{#if loading}
			<div class="text-center py-12">
				<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
			</div>
		{:else if error}
			<div class="text-center py-12 text-red-600">
				<p>Erreur: {error}</p>
			</div>
		{:else if annonces.length > 0}
			<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
				{#each annonces as annonce}
					<AnnonceCard {annonce} />
				{/each}
			</div>
		{:else}
			<div class="text-center py-12 text-gray-600">
				<p>Aucune annonce disponible pour le moment.</p>
			</div>
		{/if}
	</div>
</section>

<!-- How It Works -->
<section class="container mx-auto px-4 py-12 md:py-16">
	<h2 class="text-2xl md:text-3xl font-bold text-center mb-8 md:mb-12">Comment ça marche ?</h2>
	
	<div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-5xl mx-auto">
		<div class="text-center">
			<div class="bg-primary text-white w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center text-xl md:text-2xl font-bold mx-auto mb-3 md:mb-4">
				1
			</div>
			<h3 class="text-lg md:text-xl font-semibold mb-2">Créez votre compte</h3>
			<p class="text-sm md:text-base text-gray-600">Inscrivez-vous gratuitement en quelques secondes</p>
		</div>
		
		<div class="text-center">
			<div class="bg-primary text-white w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center text-xl md:text-2xl font-bold mx-auto mb-3 md:mb-4">
				2
			</div>
			<h3 class="text-lg md:text-xl font-semibold mb-2">Déposez votre annonce</h3>
			<p class="text-sm md:text-base text-gray-600">Ajoutez des photos et décrivez votre article</p>
		</div>
		
		<div class="text-center">
			<div class="bg-primary text-white w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center text-xl md:text-2xl font-bold mx-auto mb-3 md:mb-4">
				3
			</div>
			<h3 class="text-lg md:text-xl font-semibold mb-2">Vendez facilement</h3>
			<p class="text-sm md:text-base text-gray-600">Discutez avec les acheteurs et finalisez la vente</p>
		</div>
	</div>
</section>
