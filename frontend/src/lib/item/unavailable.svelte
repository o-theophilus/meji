<script>
	import { page } from '$app/stores';
	import { token } from '$lib/cookie.js';
	import { user, toast, loading, state } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';

	export let item;

	const submit = async () => {
		$loading = true;
		$user.saves = $user.saves.filter((i) => i != item.key);

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/save`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				save: false
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user.saves = resp.user.saves;

			let i = $state.findIndex((x) => x.name == 'save');
			if (i != -1) {
				$state[i].loaded = false;
			}
		} else {
			$toast = {
				status: 400,
				message: 'Error saving item'
			};
		}
	};
</script>

<div class="blocker">
	<div class="block">
		Unavailable
		{#if $user.permissions.includes('item:edit_status') || ($page.url.pathname == '/save' && $user.saves.includes(item.key))}
			<div class="button">
				{#if $user.permissions.includes('item:edit_status')}
					<Button size="small" href="/{item.slug}">view</Button>
				{/if}
				{#if $page.url.pathname == '/save' && $user.saves.includes(item.key)}
					<Button size="small" extra="hover_red" on:click={submit}>Remove</Button>
				{/if}
			</div>
		{/if}
	</div>
</div>

<style>
	.blocker {
		display: flex;
		justify-content: center;
		align-items: center;

		position: absolute;
		inset: 0;
		background-color: color-mix(in srgb, var(--ac4), transparent 40%);
		color: var(--ac1);
	}
	.block {
		display: grid;
		gap: var(--sp1);
		justify-items: center;

		padding: var(--sp2);
		border-radius: var(--sp0);
		background-color: var(--ac6);
	}

	.button {
		display: flex;
		gap: var(--sp1);

		pointer-events: all;
	}
</style>
