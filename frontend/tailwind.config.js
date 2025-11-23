/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: '#FF6B35',
				secondary: '#004E89',
				accent: '#F7B801',
				success: '#06D6A0',
				warning: '#FFD23F',
				danger: '#EF476F'
			},
			fontFamily: {
				sans: ['Inter', 'sans-serif']
			}
		}
	},
	plugins: [
		require('@tailwindcss/forms'),
		require('@tailwindcss/typography')
	]
};
