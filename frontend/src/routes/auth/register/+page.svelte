<script>
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';
	import { api } from '$lib/api/client';
	
	let formData = {
		email: '',
		password: '',
		first_name: '',
		last_name: '',
		phone: '',
		city: ''
	};
	let confirmPassword = '';
	let error = '';
	let loading = false;
	
	async function handleRegister() {
		error = '';
		
		// Validation
		if (formData.password !== confirmPassword) {
			error = 'Les mots de passe ne correspondent pas';
			return;
		}
		
		if (formData.password.length < 6) {
			error = 'Le mot de passe doit contenir au moins 6 caractères';
			return;
		}
		
		loading = true;
		
		try {
			// Register
			await api.post('/auth/register', formData);
			
			// Auto login
			const loginFormData = new FormData();
			loginFormData.append('username', formData.email);
			loginFormData.append('password', formData.password);
			
			const response = await fetch('/api/v1/auth/login', {
				method: 'POST',
				body: loginFormData
			});
			
			if (!response.ok) {
				throw new Error('Registration successful but login failed. Please login manually.');
			}
			
			const tokenData = await response.json();
			const userData = await api.get('/users/me');
			
			login(userData, tokenData.access_token);
			goto('/');
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Inscription - MadSugu</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				Créer un compte
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				Ou
				<a href="/auth/login" class="font-medium text-primary hover:text-primary/90">
					connectez-vous à votre compte existant
				</a>
			</p>
		</div>
		
		<form class="mt-8 space-y-6" on:submit|preventDefault={handleRegister}>
			{#if error}
				<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
					{error}
				</div>
			{/if}
			
			<div class="space-y-4">
				<div class="grid grid-cols-2 gap-4">
					<div>
						<label for="first_name" class="block text-sm font-medium text-gray-700 mb-1">
							Prénom
						</label>
						<input
							id="first_name"
							type="text"
							bind:value={formData.first_name}
							class="input"
							placeholder="Prénom"
						/>
					</div>
					
					<div>
						<label for="last_name" class="block text-sm font-medium text-gray-700 mb-1">
							Nom
						</label>
						<input
							id="last_name"
							type="text"
							bind:value={formData.last_name}
							class="input"
							placeholder="Nom"
						/>
					</div>
				</div>
				
				<div>
					<label for="email" class="block text-sm font-medium text-gray-700 mb-1">
						Email *
					</label>
					<input
						id="email"
						type="email"
						required
						bind:value={formData.email}
						class="input"
						placeholder="votre@email.com"
					/>
				</div>
				
				<div>
					<label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
						Téléphone
					</label>
					<input
						id="phone"
						type="tel"
						bind:value={formData.phone}
						class="input"
						placeholder="+221 XX XXX XX XX"
					/>
				</div>
				
				<div>
					<label for="city" class="block text-sm font-medium text-gray-700 mb-1">
						Ville
					</label>
					<input
						id="city"
						type="text"
						bind:value={formData.city}
						class="input"
						placeholder="Dakar, Abidjan, Bamako..."
					/>
				</div>
				
				<div>
					<label for="password" class="block text-sm font-medium text-gray-700 mb-1">
						Mot de passe *
					</label>
					<input
						id="password"
						type="password"
						required
						bind:value={formData.password}
						class="input"
						placeholder="••••••••"
					/>
				</div>
				
				<div>
					<label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-1">
						Confirmer le mot de passe *
					</label>
					<input
						id="confirm_password"
						type="password"
						required
						bind:value={confirmPassword}
						class="input"
						placeholder="••••••••"
					/>
				</div>
			</div>
			
			<div class="flex items-center">
				<input
					id="terms"
					name="terms"
					type="checkbox"
					required
					class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
				/>
				<label for="terms" class="ml-2 block text-sm text-gray-900">
					J'accepte les <a href="/cgu" class="text-primary hover:underline">conditions d'utilisation</a>
				</label>
			</div>
			
			<div>
				<button
					type="submit"
					disabled={loading}
					class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
				>
					{loading ? 'Inscription...' : "S'inscrire"}
				</button>
			</div>
		</form>
	</div>
</div>
