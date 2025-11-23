<script>
	import { formatPrice, getTimeAgo } from '$lib/utils/format';
	
	export let annonce;
	export let showFavorite = true;
	
	let isFavorite = false;
	
	const imageUrl = annonce.images?.[0]?.url || '/placeholder.jpg';
</script>

<a href="/annonces/{annonce.id}" class="block">
	<div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
		<div class="relative">
			<img 
				src={imageUrl} 
				alt={annonce.title}
				class="w-full h-48 object-cover"
				loading="lazy"
			/>
			{#if showFavorite}
				<button 
					class="absolute top-2 right-2 p-2 bg-white rounded-full shadow-md hover:bg-gray-50"
					on:click|preventDefault={() => isFavorite = !isFavorite}
				>
					<svg class="w-5 h-5 {isFavorite ? 'fill-red-500' : 'fill-gray-300'}" viewBox="0 0 24 24">
						<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
					</svg>
				</button>
			{/if}
			{#if annonce.is_featured}
				<span class="absolute top-2 left-2 bg-yellow-400 text-xs font-semibold px-2 py-1 rounded">
					URGENT
				</span>
			{/if}
		</div>
		
		<div class="p-4">
			<h3 class="font-semibold text-lg mb-2 truncate">{annonce.title}</h3>
			<p class="text-2xl font-bold text-primary mb-2">
				{formatPrice(annonce.price)} FCFA
			</p>
			<div class="flex items-center text-sm text-gray-600 mb-2">
				<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
				</svg>
				<span>{annonce.location_city || 'Non spécifié'}</span>
			</div>
			<div class="text-xs text-gray-500">
				{getTimeAgo(annonce.created_at)}
			</div>
		</div>
	</div>
</a>
