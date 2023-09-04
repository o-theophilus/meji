<script>
	import { token } from '$lib/cookie.js';
	import { loading } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$token = resp.token;
			document.location = '/';
		}
	};
</script>

<Button
	class="tiny"
	name="Logout"
	on:click={() => {
		submit();
	}}
/>
