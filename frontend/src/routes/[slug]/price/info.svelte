<script>
	export let item;
</script>

<dir class="details">
	<div>Maximum Price</div>
	<div>₦{item.price_old.toLocaleString()}</div>

	<div>Selling Price</div>
	<div>₦{item.price.toLocaleString()}</div>

	<div>Discount</div>
	{#if item.price && item.price_old}
		<div>{(((item.price_old - item.price) * 100) / item.price_old).toFixed(0)}% off</div>
	{:else}
		<div>0% off</div>
	{/if}

	<div class="hr"></div>

	<div>Total</div>
	<div>₦{item.price.toLocaleString()}</div>

	<div class="hr"></div>

	<div>Overall save</div>
	<div>₦{(item.price_old - item.price).toLocaleString()}</div>
</dir>

<style>
	.details {
		display: grid;
		gap: var(--sp1) var(--sp2);
		grid-template-columns: 1fr auto;

		background-color: var(--input);
		padding: var(--sp2);
		border-radius: var(--sp1);

		font-size: small;
	}
	.hr {
		grid-column: 1/3;
		height: 1px;
		background-color: var(--overlay);
	}
</style>
