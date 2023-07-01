<script>
	import Button from '$lib/comp/button.svelte';
	import SVG from '$lib/comp/svg.svelte';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	export let item;
	let _type = 1;
	export { _type as type };

	const submit = async () => {
		if (item.save) {
			$user.saves = $user.saves.filter((i) => i.key != item.key);
		} else {
			$user.saves.push(item);
			$user = $user;
		}

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}save/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user = resp.data.user;
			} else {
				new Error(resp.message);
			}
		}
	};
</script>

{#if _type == 1}
	<Button
		color={item.save ? 'var(--color2)' : ''}
		icon="like_active"
		icon_size="12"
		on:click={() => {
			submit();
		}}
	/>
{:else}
	<div class:save={item.save} on:keypress on:click|stopPropagation={submit}>
		<SVG type="like_active" />
	</div>
{/if}

<style>
	div {
		padding: var(--gap1);
		width: 100%;

		text-align: center;
		fill: var(--midtone);
	}
	div:hover {
		background-color: var(--background);
	}
	div.save {
		fill: var(--color1);
	}
</style>
