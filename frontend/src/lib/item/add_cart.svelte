<script>
	import { user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/comp/svg.svelte';
	import Variation from './add_cart__variation.svelte';

	export let item = {};
	let _type = 1;
	export { _type as type };
</script>

{#if _type == 1}
	<Button
		name="Add to cart"
		icon="cart_add"
		class="primary"
		on:click={() => {
			$module = {
				module: Variation,
				item
			};
		}}
	/>
{:else}
	<button
		class="cart"
		on:click|stopPropagation={() => {
			$module = {
				module: Variation,
				item
			};
		}}
	>
		<SVG type="cart_active" />
	</button>
{/if}

<style>
	button {
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
