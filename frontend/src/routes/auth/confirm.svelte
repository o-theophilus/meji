<script>
	import { module, loading } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';

	onMount(async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm/${$module.token}`);
		resp = await resp.json();
		$loading = false;

		let title = 'Email Confirmed';
		let message =
			resp.status == 200 && resp.error ? resp.error : 'your email confirmation was successful.';

		if (resp.status != 200) {
			title = 'Invalid or Expired Token';
			message = `
	**Invalid or Expired Token**;
	There was an error while reading the token.
	
	Please Login again to repeat the process.`;
		}

		$module = {
			module: Info,
			status: resp.status,
			title,
			message,
			button: [
				{
					name: 'Login',
					icon: 'ok',
					fn: () => {
						$module = {
							module: Login,
							email: resp.user.email
						};
					}
				}
			]
		};
	});
</script>
