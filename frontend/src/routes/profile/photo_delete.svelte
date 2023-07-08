<script>
	import { token } from '$lib/cookie.js';
	import {  module, tick } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Info from '$lib/module/info.svelte';

	export let user;
	let error;

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/photo_user/${user.key}`, {
			method: 'delete',
			headers: {
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.user);

				$module = {
					module: Info,
					data: {
						status: 'good',
						title: 'Photo Removed',
						message: `photo has been removed successfully`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Button
	class="tiny"
	icon="close"
	icon_size="8"
	on:click={() => {
		submit();
	}}
/>

<style>
</style>