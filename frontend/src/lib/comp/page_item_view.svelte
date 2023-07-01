<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	let item_view = 'grid';
	if ($user) {
		item_view = $user.setting.item_view;
	}

	const submit = async () => {
		item_view = item_view == 'grid' ? 'list' : 'grid';
		$user.setting.item_view = item_view;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ item_view })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user.setting.item_view = resp.data.user.setting.item_view;
			}
		}
	};
</script>

<div on:click={submit}>{item_view}</div>

<style>
	* {
		color: var(--font1);
	}
</style>
