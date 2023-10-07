<script>
	import Value from '$lib/item/variation_value.svelte';

	export let order;
</script>

<div class="grid">
	<div class="th">s/n</div>
	<div class="th left">Name</div>
	<div class="th">Price</div>
	<div class="th">Qty</div>
	<div class="th">Cost</div>

	{#each order.items as item, i}
		<div>
			{i + 1}
		</div>
		<a class="left" href="/{item.slug}" data-sveltekit-preload-data="tap">
			<span class="bold">
				{item.name}
			</span>
			{#if Object.keys(item.variation).length > 0}
				-
				{#each Object.entries(item.variation) as [key, value], i}
					{#if i != 0},&nbsp;{/if}
					{key}: <Value {value} />
				{/each}
			{/if}
		</a>

		<div class="right">
			₦{item.price.toLocaleString()}
		</div>
		<div>
			{item.quantity}
		</div>
		<div class="right">
			₦{(item.price * item.quantity).toLocaleString()}
		</div>
	{/each}

	<div>{order.items.length + 1}</div>
	<div class="bold left">Delivery Fee</div>
	<span />
	<span />
	<div class="right">₦{order.info.delivery_fee.toLocaleString()}</div>
	<span />
	<span />
	<span />
	<div class="bold left">Total</div>
	<div class="bold right">
		₦{(order.info.total_items + order.info.delivery_fee).toLocaleString()}
	</div>
</div>

<style>
	.grid {
		display: grid;
		gap: var(--sp1) var(--sp3);
		grid-template-columns: repeat(5, 1fr);
		grid-template-columns: auto 1fr auto auto auto;

		text-align: center;
	}

	.th {
		color: var(--ac1);
	}

	.right {
		text-align: right;
	}
	.left {
		text-align: left;
	}
	.bold {
		font-weight: 500;
		color: var(--ac1);
	}
	a {
		text-decoration: none;
		color: var(--ac2);
	}
</style>
