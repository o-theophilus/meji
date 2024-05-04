<script>
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Variation from './add_cart._variation.svelte';

	export let item = {};
	let _type = 1;
	export { _type as type };
</script>

{#if _type == 1}
	<Button
		primary
		on:click={() => {
			$module = {
				module: Variation,
				item
			};
		}}
	>
		<SVG type="cart_add" size="18" />
		Add to cart
	</Button>
{:else}
	<button
		title="Add to cart"
		class="cart"
		on:click={() => {
			$module = {
				module: Variation,
				item
			};
		}}
	>
		<SVG type="cart_add" />
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
</style>
