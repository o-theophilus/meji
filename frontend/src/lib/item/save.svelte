<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/comp/svg.svelte';

	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	export let item;
	let _type = 1;
	export { _type as type };

	const submit = async () => {
		let save = true;
		if ($user.saves.includes(item.key)) {
			$user.saves = $user.saves.filter((i) => i != item.key);
			save = false;
		} else {
			$user.saves.push(item.key);
			$user = $user;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/save`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				key: item.key,
				save
			})
		});

		resp = await resp.json();

		// if (resp.status == 200) {
		// 		$user = resp.user;
		// }
	};
</script>

{#if _type == 1}
	<Button
		color={$user.saves.includes(item.key) ? 'var(--cl2)' : ''}
		icon="like_active"
		icon_size="12"
		on:click={() => {
			submit();
		}}
	/>
{:else}
	<button
		class:save={$user.saves.includes(item.key)}
		on:click|stopPropagation={() => {
			submit();
		}}
	>
		<SVG type="like_active" />
	</button>
{/if}

<style>
	button {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 100%;
		border: none;

		padding: var(--sp1);
		background-color: transparent;
		fill: var(--ac3);
		cursor: pointer;
	}
	button:hover {
		background-color: var(--ac4);
	}
	button.save {
		fill: var(--cl1);
	}
</style>
