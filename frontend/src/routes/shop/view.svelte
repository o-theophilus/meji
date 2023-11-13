<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	const save_view = async () => {
		$user.setting.item_view = $user.setting.item_view == 'grid' ? 'list' : 'grid';
		const resp = await fetch(`${import.meta.env.VITE_BACKEND}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ item_view: $user.setting.item_view })
		});
	};
</script>

<Button class="outline" on:click={save_view}>
	<SVG type={$user.setting.item_view == 'grid' ? 'shop_active' : 'list'} />
	view
</Button>
