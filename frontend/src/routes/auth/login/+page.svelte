<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	
	let email = '';
	let password = '';
	let error = '';
	let loading = false;
	
	async function handleLogin() {
		error = '';
		loading = true;
		
		try {
			// Use form data for OAuth2
			const formData = new FormData();
			formData.append('username', email); // OAuth2 expects 'username'
			formData.append('password', password);
			
			const response = await fetch('/api/v1/auth/login', {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Login failed');
			}
			
			const tokenData = await response.json();
			
			// Get user profile
			const userData = await api.get('/users/me');
			
			// Save to store
			login(userData, tokenData.access_token);
			
			// Redirect to home
			goto('/');
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Connexion - MadSugu</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				Connexion à votre compte
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				Ou
				<a href="/auth/register" class="font-medium text-primary hover:text-primary/90">
					créez un nouveau compte
				</a>
			</p>
		</div>
		
		<form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
			{#if error}
				<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
					{error}
				</div>
			{/if}
			
			<div class="rounded-md shadow-sm space-y-4">
				<div>
					<label for="email" class="block text-sm font-medium text-gray-700 mb-1">
						Email
					</label>
					<input
						id="email"
						name="email"
						type="email"
						required
						bind:value={email}
						class="input"
						placeholder="votre@email.com"
					/>
				</div>
				
				<div>
					<label for="password" class="block text-sm font-medium text-gray-700 mb-1">
						Mot de passe
					</label>
					<input
						id="password"
						name="password"
						type="password"
						required
						bind:value={password}
						class="input"
						placeholder="••••••••"
					/>
				</div>
			</div>
			
			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<input
						id="remember-me"
						name="remember-me"
						type="checkbox"
						class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
					/>
					<label for="remember-me" class="ml-2 block text-sm text-gray-900">
						Se souvenir de moi
					</label>
				</div>
				
				<div class="text-sm">
					<a href="/auth/forgot-password" class="font-medium text-primary hover:text-primary/90">
						Mot de passe oublié ?
					</a>
				</div>
			</div>
			
			<div>
				<button
					type="submit"
					disabled={loading}
					class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
				>
					{loading ? 'Connexion...' : 'Se connecter'}
				</button>
			</div>
		</form>
	</div>
</div>
