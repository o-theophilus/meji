<script>
	export let cart;
</script>

<section>
	<img src="/image/item.png" alt="delivery" />
	<div class="details">
		<div>Delivery fee</div>
		<div>
			₦{cart.transaction.delivery_fee.toLocaleString()}
		</div>
	</div>
</section>

<style>
	section {
		--height: 80px;
		display: flex;
		gap: var(--sp3);
		align-items: center;
	}

	img {
		width: var(--height);
		height: var(--height);

		border-radius: var(--sp0);
	}
	.details {
		display: flex;
		justify-content: space-between;

		width: 100%;
		/* min-height: var(--height); */
	}
</style>
