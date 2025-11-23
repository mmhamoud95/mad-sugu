/**
 * Format price in FCFA
 */
export function formatPrice(price) {
	return new Intl.NumberFormat('fr-FR').format(price);
}

/**
 * Get relative time string
 */
export function getTimeAgo(date) {
	const now = new Date();
	const past = new Date(date);
	const diffInSeconds = Math.floor((now - past) / 1000);
	
	if (diffInSeconds < 60) {
		return 'À l\'instant';
	}
	
	const diffInMinutes = Math.floor(diffInSeconds / 60);
	if (diffInMinutes < 60) {
		return `Il y a ${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''}`;
	}
	
	const diffInHours = Math.floor(diffInMinutes / 60);
	if (diffInHours < 24) {
		return `Il y a ${diffInHours} heure${diffInHours > 1 ? 's' : ''}`;
	}
	
	const diffInDays = Math.floor(diffInHours / 24);
	if (diffInDays < 7) {
		return `Il y a ${diffInDays} jour${diffInDays > 1 ? 's' : ''}`;
	}
	
	const diffInWeeks = Math.floor(diffInDays / 7);
	if (diffInWeeks < 4) {
		return `Il y a ${diffInWeeks} semaine${diffInWeeks > 1 ? 's' : ''}`;
	}
	
	const diffInMonths = Math.floor(diffInDays / 30);
	if (diffInMonths < 12) {
		return `Il y a ${diffInMonths} mois`;
	}
	
	const diffInYears = Math.floor(diffInDays / 365);
	return `Il y a ${diffInYears} an${diffInYears > 1 ? 's' : ''}`;
}

/**
 * Truncate text to specified length
 */
export function truncate(text, length = 100) {
	if (text.length <= length) return text;
	return text.substring(0, length) + '...';
}
