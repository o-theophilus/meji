<script>
	import { goto } from '$app/navigation';
	import { loading } from '$lib/store.js';

	import SVG from '$lib/comp/svg2.svelte';

	export let tag = '';
</script>

<button
	on:click={() => {
		$loading = true;
		goto(`/shop?${new URLSearchParams(`tag=${tag}`).toString()}`);
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
		border: 2px solid var(--ac4);

		color: var(--ac2);
		fill: var(--ac2);
		background-color: transparent;
		border-radius: var(--sp0);
		cursor: pointer;
		text-align: center;
		text-transform: capitalize;
	}
	button:hover {
		color: var(--ac1);
		fill: var(--ac1);
		border-color: var(--cl1);
	}

	@media screen and (min-width: 700px) {
		button {
			height: 150px;
		}
	}
</style>
