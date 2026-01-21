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
		gap: var(--sp1) var(--sp2);
		grid-template-columns: 1fr auto;

		background-color: var(--bg3);
		padding: var(--sp2);
		border-radius: var(--sp1);
		outline: 1px solid var(--bg2);
		outline-offset: -1px;

		font-size: small;
	}
	.hr {
		grid-column: 1/3;
		height: 1px;
		background-color: var(--overlay);
	}
</style>
