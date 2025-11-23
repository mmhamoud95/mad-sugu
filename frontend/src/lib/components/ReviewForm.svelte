<script>
	export let userId;
	export let annonceId = null;
	export let onSubmit = null;
	
	let rating = 5;
	let comment = '';
	let loading = false;
	let error = null;
	let success = false;
	
	async function handleSubmit() {
		loading = true;
		error = null;
		success = false;
		
		try {
			const token = localStorage.getItem('token');
			if (!token) {
				error = 'Vous devez être connecté pour laisser un avis';
				return;
			}
			
			const response = await fetch('http://localhost:8000/api/v1/reviews/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					reviewed_user_id: userId,
					rating: rating,
					comment: comment || null,
					annonce_id: annonceId
				})
			});
			
			if (response.ok) {
				success = true;
				comment = '';
				rating = 5;
				if (onSubmit) onSubmit();
			} else {
				const data = await response.json();
				error = data.detail || 'Erreur lors de l\'envoi de l\'avis';
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
	<h3 class="text-xl font-semibold mb-4">Laisser un avis</h3>
	
	{#if success}
		<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
			Merci pour votre avis !
		</div>
	{/if}
	
	{#if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
			{error}
		</div>
	{/if}
	
	<form on:submit|preventDefault={handleSubmit}>
		<!-- Star rating -->
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2">
				Note
			</label>
			<div class="flex items-center space-x-2">
				{#each [1, 2, 3, 4, 5] as star}
					<button
						type="button"
						on:click={() => rating = star}
						class="text-3xl transition-all {star <= rating ? 'text-yellow-400' : 'text-gray-300'} hover:scale-110"
					>
						⭐
					</button>
				{/each}
				<span class="ml-2 text-gray-600">({rating}/5)</span>
			</div>
		</div>
		
		<!-- Comment -->
		<div class="mb-4">
			<label for="comment" class="block text-gray-700 text-sm font-bold mb-2">
				Commentaire (optionnel)
			</label>
			<textarea
				id="comment"
				bind:value={comment}
				rows="4"
				maxlength="1000"
				class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
				placeholder="Partagez votre expérience..."
			></textarea>
			<p class="text-sm text-gray-500 mt-1">{comment.length}/1000 caractères</p>
		</div>
		
		<!-- Submit button -->
		<button
			type="submit"
			disabled={loading}
			class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
		>
			{loading ? 'Envoi en cours...' : 'Envoyer l\'avis'}
		</button>
	</form>
</div>
