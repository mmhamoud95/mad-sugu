<script>
	import { onMount } from 'svelte';
	
	export let userId;
	
	let reviews = [];
	let loading = true;
	let error = null;
	
	onMount(async () => {
		await fetchReviews();
	});
	
	async function fetchReviews() {
		loading = true;
		error = null;
		
		try {
			const response = await fetch(`http://localhost:8000/api/v1/reviews/user/${userId}`);
			
			if (response.ok) {
				reviews = await response.json();
			} else {
				error = 'Erreur lors du chargement des avis';
			}
		} catch (err) {
			error = 'Erreur de connexion';
			console.error(err);
		} finally {
			loading = false;
		}
	}
	
	function formatDate(dateString) {
		const date = new Date(dateString);
		return date.toLocaleDateString('fr-FR', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}
	
	function renderStars(rating) {
		return '⭐'.repeat(Math.floor(rating));
	}
</script>

<div class="bg-white rounded-lg shadow-md p-6">
	<h3 class="text-xl font-semibold mb-4">
		Avis ({reviews.length})
	</h3>
	
	{#if loading}
		<div class="text-center py-8">
			<div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
			<p class="mt-2 text-gray-600">Chargement des avis...</p>
		</div>
	{:else if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
			{error}
		</div>
	{:else if reviews.length === 0}
		<div class="text-center py-8 text-gray-500">
			Aucun avis pour le moment
		</div>
	{:else}
		<div class="space-y-4">
			{#each reviews as review}
				<div class="border-b border-gray-200 pb-4 last:border-b-0">
					<div class="flex items-start justify-between mb-2">
						<div>
							<div class="flex items-center space-x-2">
								<span class="text-lg">{renderStars(review.rating)}</span>
								<span class="text-gray-600">({review.rating}/5)</span>
							</div>
						</div>
						<span class="text-sm text-gray-500">
							{formatDate(review.created_at)}
						</span>
					</div>
					
					{#if review.comment}
						<p class="text-gray-700 mt-2">
							{review.comment}
						</p>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>
