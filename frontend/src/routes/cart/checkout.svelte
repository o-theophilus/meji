<script>
	import { app } from '$lib/store.svelte.js';
	import { Button } from '$lib/button';

	let total = $derived.by(() => {
		let temp = 0;
		for (const i of app.cart_items) {
			temp += i.price * i.quantity;
		}
		return temp;
	});
</script>

<div class="floater">
	<div class="floater_block">
		<div class="line space">
			<div class="total">Total Amount</div>
			<div class="price">₦{total.toLocaleString()}</div>
		</div>

		<div class="checkout">
			<Button
				icon="cart"
				--button-color="white"
				--button-background-color="var(--cl1)"
				onclick={() => {
					console.log('checkout');
				}}
			>
				Checkout
			</Button>
		</div>
	</div>
</div>

<style>
	.floater {
		position: sticky;
		bottom: var(--headerHeight);

		background-color: var(--bg1);
		border-top: 1px solid var(--bg2);
	}

	.floater_block {
		padding: 16px 24px;
		max-width: var(--mobileWidth);
		margin: auto;
	}

	.total {
		font-size: 0.8rem;
	}
	.price {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}

	.checkout {
		display: flex;
		justify-content: flex-end;
		margin-top: 16px;
	}
</style>
