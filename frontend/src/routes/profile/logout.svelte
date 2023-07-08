<script>
	import { token } from '$lib/cookie.js';
	import { user } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/logout`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$token = resp.token;
			$user = resp.user;
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
