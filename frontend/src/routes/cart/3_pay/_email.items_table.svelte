<script>
	import Value from '../../[slug]/variation/value.svelte';
	let { items = [] } = $props();
</script>

<hr style="border-color: gray; margin: 24px 0;" />

<b style="font-size: 0.8rem;">Item{items.length ? 's' : ''}:</b>
<br />
<br />

<div style="display: grid; gap: var(--sp1) var(--sp1); grid-template-columns: auto 1fr auto auto;">
	<div style="text-align: center; font-size: 0.8rem;">s/n</div>
	<div style="text-align: left; font-size: 0.8rem;">Name</div>
	<div style="text-align: center; font-size: 0.8rem;">Price</div>
	<div style="text-align: center; font-size: 0.8rem;">Qty</div>

	{#each items as item, i}
		<div style="text-align: center;">
			{i + 1}
		</div>
		<span>
			<a href="/{item.slug}" style="text-decoration: none; color: var(--cl1);">
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

		<div style="text-align: right;">
			₦{item.price.toLocaleString()}
		</div>
		<div style="text-align: center;">
			{item.quantity}
		</div>
	{/each}
</div>
