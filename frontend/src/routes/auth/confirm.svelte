<script>
	import { module, loading } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Login from './login.svelte';
	import Info from '$lib/module/info.svelte';

	onMount(async () => {
		$loading = 'loading . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/confirm/${$module.token}`);
		$loading = false;
		resp = await resp.json();

		if (resp.status == 200) {
			$module = {
				module: Login,
				message: resp.error || 'your email confirmation was successful.',
				email: resp.user.email
			};
		} else {
			$module = {
				module: Info,
				status: 401,
				title: `Invalid or Expired Token`,
				message: `
**Invalid or Expired Token**;
There was an error while reading the token.

Please try again repeacting the action.`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		}
	});
</script>
