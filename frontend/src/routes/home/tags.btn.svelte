<script>
	import { goto } from '$app/navigation';
	import { loading, state } from '$lib/store.js';

	import SVG from '$lib/svg_tags.svelte';

	export let tag = '';
</script>

<button
	on:click={() => {
		let i = $state.findIndex((x) => x.name == 'shop');
		if (i != -1) {
			$state[i].search = `?${new URLSearchParams({ tag }).toString()}`;
			$state[i].loaded = false;
		}

		$loading = 'loading . . .';
		goto('/shop');
	}}
>
	<SVG type={tag.toLowerCase()} size="30" />
	{tag}
</button>

<style>
	button {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);

		height: 100px;
		width: 100%;
		padding: var(--sp2);
		border: none;

		outline: 2px solid var(--ac4);
		fill: currentColor;
		background-color: transparent;
		border-radius: var(--sp0);
		cursor: pointer;
		text-align: center;
		text-transform: capitalize;
		color: var(--ac2);
	}
	button:hover {
		color: var(--ac1);
		fill: var(--ac1);
		outline-color: var(--ac1);
	}

	@media screen and (min-width: 700px) {
		button {
			height: 150px;
		}
	}
</style>
