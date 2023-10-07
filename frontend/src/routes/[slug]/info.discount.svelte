<script>
	export let item;
</script>

<br />
<dir class="details">
	<div>Maximum Price</div>
	<div>₦{item.old_price.toLocaleString()}</div>

	<div>Selling Price</div>
	<div>₦{item.price.toLocaleString()}</div>

	<div>Discount</div>
	<div>{(((item.old_price - item.price) * 100) / item.old_price).toFixed(0)}% off</div>

	<div class="hr" />

	<div>Total</div>
	<div>₦{item.price.toLocaleString()}</div>

	<div class="hr" />

	<div>Overall save</div>
	<div>₦{(item.old_price - item.price).toLocaleString()}</div>
</dir>

<style>
	.details {
		display: grid;
		gap: var(--sp1) var(--sp2);
		grid-template-columns: 1fr auto;

		font-size: small;
	}
	.hr {
		grid-column: 1/3;
		height: 1px;
		background-color: var(--ac4);
	}
</style>
