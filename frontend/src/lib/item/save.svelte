<script>
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import { user, toast, loading, state } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	export let item;
	let _type = 1;
	export { _type as type };

	const submit = async () => {
		$loading = true;

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

{#if _type == 1}
	<Button class="round large" on:click={submit}>
		<div class:save={$user.saves.includes(item.key)}>
			<SVG type="like_active" size="12" />
		</div>
	</Button>
{:else}
	<button title="save" class:save={$user.saves.includes(item.key)} on:click={submit}>
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
	.save {
		fill: var(--cl1);
	}
</style>
