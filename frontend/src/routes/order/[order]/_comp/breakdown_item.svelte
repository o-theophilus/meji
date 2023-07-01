<script>
	import { currency } from '$lib/store.js';

	import Value from '$lib/comp/variation_value.svelte';

	export let items;

	const proc = (v) => v.split(':');
</script>

<div class="grid">
	<div class="th">s/n</div>
	<div class="th">Name</div>
	<div class="th">Price</div>
	<div class="th">Qty</div>
	<div class="th">Cost</div>
	{#each items as item, i}
		<div class="num">
			{i + 1}
		</div>
		<div class="h name">
			<a href="/{item.alias}">
				{item.name}
			</a>

			<Value variation={item.variation} />
		</div>
		<div class="price">
			{currency(item.price)}
		</div>
		<div class="num">
			{item.quantity}
		</div>
		<div class="price">
			{currency(item.price * item.quantity)}
		</div>
	{/each}
</div>

<style>
	.grid {
		display: grid;
		gap: var(--gap1) var(--gap3);
		grid-template-columns: repeat(5, 1fr);
		grid-template-columns: auto 1fr auto auto auto;
	}

	.th {
		font-weight: 500;
		text-align: center;
	}

	.num {
		text-align: center;
	}
	.price {
		text-align: right;
	}
	a {
		color: var(--font1);
		text-decoration: none;
	}
	.name {
		justify-content: center;
		gap: 4px;
	}
</style>
