<script>
	import Button from '$lib/comp/button.svelte';
	import SVG from '$lib/comp/svg.svelte';

	import { user, save_queue } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let item;
	let _type = 1;
	export { _type as type };

	const submit = async () => {
		if (item.saved) {
			$user.saves = $user.saves.filter((i) => i != item.key);
			emit('unsaved');
		} else {
			$user.saves.push(item.key);
			$user = $user;
		}

		$save_queue.push(item.key);

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/save`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ saves: $user.saves })
		});

		resp = await resp.json();

		if (resp.status == 200) {
			$save_queue = $save_queue.filter((x) => x != item.key);
			if ($save_queue.length == 0) {
				$user = resp.user;
				emit('done', { items: resp.items });
			}
		} else {
			new Error(resp.message);
		}
	};

	$: {
		item.saved = false;
		for (let i in $user.saves) {
			if ($user.saves[i] == item.key) {
				item.saved = true;
				break;
			}
		}
	}
</script>

{#if _type == 1}
	<Button
		color={item.saved ? 'var(--color2)' : ''}
		icon="like_active"
		icon_size="12"
		on:click={() => {
			submit();
		}}
	/>
{:else}
	<button
		class:save={item.saved}
		on:click|stopPropagation={() => {
			submit();
		}}
	>
		<SVG type="like_active" />
	</button>
{/if}

<style>
	button {
		width: 100%;
		border: none;
		padding: var(--gap1);

		background-color: transparent;
		fill: var(--midtone);
		cursor: pointer;
	}
	button:hover {
		background-color: var(--background);
	}
	button.save {
		fill: var(--color1);
	}
</style>
