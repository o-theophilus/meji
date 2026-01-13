<script>
	import Value from '../../[slug]/variation/value.svelte';
	let { items = [] } = $props();
</script>

<div class="grid">
	<div class="th">s/n</div>
	<div class="th left">Name</div>
	<div class="th">Price</div>
	<div class="th">Qty</div>
	<div class="th">Cost</div>

	{#each items as item, i}
		<div>
			{i + 1}
		</div>
		<span class="left">
			<a href="/{item.slug}">
				{item.name}
			</a>
			{#if Object.keys(item.variation).length > 0}
				-
				{#each Object.entries(item.variation) as [key, value], i}
					{#if i != 0},&nbsp;{/if}
					{key}: <Value {value} small></Value>
				{/each}
			{/if}
		</span>

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
</div>

<style>
	.grid {
		display: grid;
		gap: var(--sp1) var(--sp1);
		grid-template-columns: auto 1fr auto auto auto;

		text-align: center;
		font-size: 0.8rem;
	}

	.right {
		text-align: right;
	}
	.left {
		text-align: left;
	}

	a {
		text-decoration: none;
		color: var(--cl1);
	}
</style>
