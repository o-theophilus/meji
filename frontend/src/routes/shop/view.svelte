<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	const save_view = async () => {
		$user.setting_item_view = $user.setting_item_view == 'grid' ? 'list' : 'grid';
		const resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/setting`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ item_view: $user.setting_item_view })
		});
	};
</script>

<Button class="outline" on:click={save_view}>
	<SVG type={$user.setting_item_view == 'grid' ? 'shop_active' : 'list'} />
	view
</Button>
