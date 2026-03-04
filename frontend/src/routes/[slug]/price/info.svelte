<script>
	import { Form } from '$lib/layout';
	import { module } from '$lib/store.svelte.js';
	let item = module.value.item;
</script>

<Form title="Price Information">
	<dir class="details">
		<div>Maximum Price</div>
		<div>₦{Number(item.price_old).toLocaleString()}</div>

		<div>Selling Price</div>
		<div>₦{Number(item.price).toLocaleString()}</div>

		<div>Discount</div>
		{#if Number(item.price) && Number(item.price_old)}
			<div>
				{(((Number(item.price_old) - Number(item.price)) * 100) / Number(item.price_old)).toFixed(
					0
				)}% off
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
</Form>

<style>
	.details {
		display: grid;
		gap: 8px 16px;
		grid-template-columns: 1fr auto;

		font-size: small;
	}
	.hr {
		grid-column: 1/3;
		height: 1px;
		background-color: var(--overlay);
	}
</style>
