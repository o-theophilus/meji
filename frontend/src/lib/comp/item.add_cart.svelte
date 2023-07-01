<script>
	import { user, module } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import SVG from '$lib/comp/svg.svelte';
	import Variation from '$lib/comp/item.add_cart.variation.svelte';

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
	<div
		class="cart"
		on:keypress
		on:click|stopPropagation={() => {
			$module = {
				module: Variation,
				item
			};
		}}
	>
		<SVG type="cart_active" />
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
</style>
