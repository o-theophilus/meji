<script>
	import Value from '$lib/item/variation_value.svelte';

	export let order;
</script>

<div class="grid">
	<div class="th">s/n</div>
	<div class="th">Name</div>
	<div class="th">Price</div>
	<div class="th">Qty</div>
	<div class="th">Cost</div>
	{#each order.items as item, i}
		<div class="num">
			{i + 1}
		</div>
		<div>
			<a class="name" href="/{item.slug}">
				{item.name}
			</a>
			<div class="line">
				{#each Object.entries(item.variation) as [key, value], i}
					{#if i != 0},{/if}
					{key}: &nbsp;<Value {value} />
				{/each}
			</div>
		</div>
		<div class="price">
			₦{item.price.toLocaleString()}
		</div>
		<div class="num">
			{item.quantity}
		</div>
		<div class="price">
			₦{(item.price * item.quantity).toLocaleString()}
		</div>
	{/each}
	<div class="num">{order.items.length + 1}</div>
	<div class=" name">Delivery Fee</div>
	<span />
	<span />
	<div class="price">₦{order.info.delivery_fee.toLocaleString()}</div>
</div>

<style>
	.grid {
		display: grid;
		gap: var(--sp1) var(--sp3);
		grid-template-columns: repeat(5, 1fr);
		grid-template-columns: auto 1fr auto auto auto;
		color: var(--ac2);
	}

	.th {
		color: var(--ac1);
	}

	.num {
		text-align: center;
	}
	.price {
		text-align: right;
	}
	a {
		text-decoration: none;
	}
	.name {
		color: var(--ac1);
		font-weight: 500;
	}

	.line {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
	}
</style>
