<script>
	import { module } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Login from '$lib/module/login.svelte';
	import Info from '$lib/module/info.svelte';

	export let data;

	onMount(async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}confirm/${data.token}`);

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$module = {
					module: Login,
					data: {
						message: 'Your email was successfully confirmed.',
						email: resp.data.user.email
					}
				};
			} else if (resp.status == 201) {
				$module = {
					module: Login,
					data: {
						message: 'Your email has already been confirmed.',
						email: resp.data.user.email
					}
				};
			} else {
				$module = {
					module: Info,
					data: {
						status: 'bad',
						title: `Invalid or Expired Token`,
						message: `
**Invalid or Expired Token**;
There was an error while reading the token.

Please try again repeacting the action.`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			}
		}
	});
</script>
