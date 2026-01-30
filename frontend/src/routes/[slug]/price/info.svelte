<script>
	export let item;
</script>

<dir class="details">
	<div>Maximum Price</div>
	<div>₦{Number(item.price_old).toLocaleString()}</div>

	<div>Selling Price</div>
	<div>₦{Number(item.price).toLocaleString()}</div>

	<div>Discount</div>
	{#if Number(item.price) && Number(item.price_old)}
		<div>
			{(((Number(item.price_old) - Number(item.price)) * 100) / Number(item.price_old)).toFixed(0)}%
			off
		</div>
	{:else}
		<div>0% off</div>
	{/if}

	<div class="hr"></div>

	<div>Total</div>
	<div>₦{Number(item.price).toLocaleString()}</div>

	<div class="hr"></div>

	<div>Overall save</div>
	<div>₦{(Number(item.price_old) - Number(item.price)).toLocaleString()}</div>
</dir>

<style>
	.details {
		display: grid;
		gap: 8px 16px;
		grid-template-columns: 1fr auto;

		background-color: var(--bg2);
		padding: 16px;
		border-radius: 8px;
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		font-size: small;
	}
	.hr {
		grid-column: 1/3;
		height: 1px;
		background-color: var(--overlay);
	}
</style>
