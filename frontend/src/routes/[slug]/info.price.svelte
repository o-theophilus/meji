<script>
	export let item;
</script>

<div class="cost">
	<div class="price">
		{#if item.price}
			₦{item.price.toLocaleString()}
		{:else}
			<span class="no_price"> Nil </span>
		{/if}
	</div>
	{#if item.old_price}
		<div class="old_price">
			₦{item.old_price.toLocaleString()}
			<div class="strike" />
		</div>
		<div class="discount">
			{(((item.old_price - item.price) * 100) / item.old_price).toFixed(0)}% off
		</div>
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
		font-weight: 500;
		font-size: large;
	}

	.no_price {
		color: var(--cl4);
	}

	.old_price {
		position: relative;
		color: var(--ac2);
	}
	.strike {
		position: absolute;
		top: calc(50% - 0.5px);
		left: -3px;
		right: -3px;

		height: 1px;

		transform: rotate(-10deg);
		background: var(--cl4);
	}
	.discount {
		color: var(--ac2);
	}
</style>
