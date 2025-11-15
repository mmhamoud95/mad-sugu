<script>
	import { user, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	
	let mobileMenuOpen = false;
	
	function handleLogout() {
		logout();
		goto('/');
	}
</script>

<header class="bg-white shadow-md sticky top-0 z-50">
	<div class="container mx-auto px-4">
		<div class="flex items-center justify-between h-16">
			<!-- Logo -->
			<a href="/" class="flex items-center space-x-2">
				<span class="text-2xl font-bold text-primary">MadSugu</span>
			</a>
			
			<!-- Search Bar (Desktop) -->
			<div class="hidden md:flex flex-1 max-w-2xl mx-8">
				<form class="w-full" action="/recherche" method="GET">
					<div class="relative">
						<input 
							type="text" 
							name="q"
							placeholder="Rechercher une annonce..."
							class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
						/>
						<svg class="absolute left-3 top-2.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
						</svg>
					</div>
				</form>
			</div>
			
			<!-- Navigation -->
			<nav class="hidden md:flex items-center space-x-4">
				{#if $user}
					<a href="/annonces/nouvelle" class="btn-primary">
						Déposer une annonce
					</a>
					<a href="/messages" class="text-gray-700 hover:text-primary">
						Messages
					</a>
					<a href="/favoris" class="text-gray-700 hover:text-primary">
						Favoris
					</a>
					<div class="relative group">
						<button class="flex items-center space-x-2 text-gray-700 hover:text-primary">
							<img 
								src={$user.profile_image || '/default-avatar.png'} 
								alt="Profile" 
								class="w-8 h-8 rounded-full"
							/>
							<span>{$user.first_name || 'Mon compte'}</span>
						</button>
						<div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 hidden group-hover:block">
							<a href="/profil" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
								Mon profil
							</a>
							<a href="/mes-annonces" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
								Mes annonces
							</a>
							<button on:click={handleLogout} class="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100">
								Déconnexion
							</button>
						</div>
					</div>
				{:else}
					<a href="/auth/login" class="text-gray-700 hover:text-primary">
						Connexion
					</a>
					<a href="/auth/register" class="btn-primary">
						Inscription
					</a>
				{/if}
			</nav>
			
			<!-- Mobile Menu Button -->
			<button 
				class="md:hidden text-gray-700"
				on:click={() => mobileMenuOpen = !mobileMenuOpen}
			>
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
				</svg>
			</button>
		</div>
		
		<!-- Mobile Menu -->
		{#if mobileMenuOpen}
			<div class="md:hidden py-4 border-t">
				<div class="mb-4">
					<form action="/recherche" method="GET">
						<input 
							type="text" 
							name="q"
							placeholder="Rechercher..."
							class="w-full px-4 py-2 border border-gray-300 rounded-lg"
						/>
					</form>
				</div>
				{#if $user}
					<a href="/annonces/nouvelle" class="block py-2 text-gray-700">
						Déposer une annonce
					</a>
					<a href="/messages" class="block py-2 text-gray-700">
						Messages
					</a>
					<a href="/favoris" class="block py-2 text-gray-700">
						Favoris
					</a>
					<a href="/profil" class="block py-2 text-gray-700">
						Mon profil
					</a>
					<a href="/mes-annonces" class="block py-2 text-gray-700">
						Mes annonces
					</a>
					<button on:click={handleLogout} class="block w-full text-left py-2 text-gray-700">
						Déconnexion
					</button>
				{:else}
					<a href="/auth/login" class="block py-2 text-gray-700">
						Connexion
					</a>
					<a href="/auth/register" class="block py-2 text-gray-700">
						Inscription
					</a>
				{/if}
			</div>
		{/if}
	</div>
</header>
