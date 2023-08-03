<script>
	import Value from '$lib/item/variation_value.svelte';

	export let items;
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
			<a href="/{item.slug}">
				{item.name}
			</a>

			{#each Object.entries(item.variation) as [key, value]}
				<div class="line ppt">
					{key}: <Value {value} />
				</div>
			{/each}

			<!-- <Value variation={item.variation} /> -->
		</div>
		<div class="price">
			₦{item.price.toLocaleString()}
		</div>
		<div class="num">
			{item.quantity}
		</div>
		<div class="price">
			₦{item.price * item.quantity.toLocaleString()}
		</div>
	{/each}
</div>

<style>
	.grid {
		display: grid;
		gap: var(--sp1) var(--sp3);
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
		color: var(--ac1);
		text-decoration: none;
	}
	.name {
		justify-content: center;
		gap: 4px;
	}
</style>
