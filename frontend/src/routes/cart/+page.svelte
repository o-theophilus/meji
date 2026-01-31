<script>
	import { onMount } from 'svelte';
	import { app } from '$lib/store.svelte.js';
	import { Meta, Log, Icon } from '$lib/macro';
	import { Content } from '$lib/layout';
	import { PageNote } from '$lib/info';
	import { Button, Link } from '$lib/button';
	import Cart from './1_cart/index.svelte';
	import Receiver from './2_receiver/index.svelte';
	import Coupons from './3_coupon/index.svelte';
	import Checkout from './checkout.svelte';

	let { data } = $props();

	onMount(() => {
		app.cart_items = data.items;
	});

	let ops = $state({
		status: 'Items',
		cart: data.cart,
		error: {},
		item_ckeck() {
			for (const item of app.cart_items) {
				if (item.status != 'active' || item.quantity > item.available_quantity) {
					return false;
				}
			}
			return true;
		},
		has_receiver() {
			return !!(
				this.cart.receiver?.name &&
				this.cart.receiver?.phone &&
				this.cart.receiver?.email &&
				this.cart.receiver?.address?.address &&
				this.cart.receiver?.address?.state &&
				this.cart.receiver?.address?.country
			);
		},
		total_items() {
			let total = 0;
			for (const i of app.cart_items) {
				total += i.price * i.quantity;
			}
			return total;
		},
		coupons: [
			{ code: 'SAVE10', entity: 'items', type: 'number', value: 10 },
			{ code: 'SAVE20', entity: 'delivery', type: 'number', value: 20 },
			{ code: 'SAVE30', entity: 'delivery', type: 'percent', value: 100 }
		],
		get delivery_date() {
			const today = new Date();
			const nextWeek = new Date(today);
			return nextWeek.setDate(today.getDate() + 7);
		}
	});
</script>

<Log entity_type={'page'} />
<Meta
	title="Cart"
	description="Review your selected items, adjust quantities, and proceed securely to checkout."
/>

<Content --content-padding-top="1px">
	<div class="page_title">Cart</div>
	{#if app.cart_items.length}
		<Cart bind:ops></Cart>
		<Receiver bind:ops previous_receivers={data.previous_receivers}></Receiver>
		<Coupons bind:ops></Coupons>

		<!-- TODO check this box -->
		<span class="terms">
			By clicking the order button, you have accepred our
			<Link href="/terms" --link-font-size="0.8rem">terms and conditions</Link>
		</span>
	{:else}
		<PageNote>
			No item in cart yet
			<div class="icon">
				<Icon icon="cart" size="50" />
			</div>
			<Button href="/shop">Shop now</Button>
		</PageNote>
	{/if}
</Content>

{#if app.cart_items.length}
	<Checkout bind:ops></Checkout>
{/if}

<style>
	.page_title {
		margin: 24px 0;
	}
	.icon {
		fill: var(--ft2);
	}

	.terms {
		font-size: small;
	}
</style>
