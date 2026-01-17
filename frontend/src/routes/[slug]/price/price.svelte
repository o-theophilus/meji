<script>
	let { item, children } = $props();
</script>

<div class="cost">
	<div class="price">
		{#if Number(item.price)}
			₦{Number(item.price).toLocaleString()}
		{:else}
			<span class="no_price"> Nil </span>
		{/if}
	</div>
	{#if Number(item.price_old)}
		<div class="old_price">
			₦{Number(item.price_old).toLocaleString()}
			<div class="strike"></div>
		</div>

		{@render children()}
	{/if}
</div>

<style>
	.cost {
		display: flex;
		flex-wrap: wrap;

		align-items: center;
		gap: var(--sp2);
	}
	.price {
		font-weight: 700;
		font-size: xx-large;
		color: var(--ac1);
	}

	.no_price {
		color: var(--cl4);
	}

	.old_price {
		position: relative;
	}
	.strike {
		position: absolute;
		top: calc(50% - 0.5px);
		left: -3px;
		right: -3px;

		height: 2px;

		transform: rotate(-10deg);
		background: red;
	}
</style>
