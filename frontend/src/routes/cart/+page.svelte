<script>
	import { Button, Link } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Checkbox } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Cart from './1_cart/index.svelte';
	import Receiver from './2_receiver/index.svelte';
	import Coupons from './3_coupon/index.svelte';
	import Checkout from './checkout.svelte';
	import { get_delivery_cost } from './delivery.js';

	let { data } = $props();
	console.log(data.cart);
	

	onMount(() => {
		app.cart_items = data.items;
	});

	let ops = $state({
		status: 'Items',
		cart: data.cart,
		coupon: data.coupon,
		agree: false,
		error: {},

		get item_ckeck() {
			for (const item of app.cart_items) {
				if (item.status != 'active' || item.quantity > item.available_quantity) {
					return false;
				}
			}
			return true;
		},
		get has_receiver() {
			return !!(
				this.cart.receiver?.name &&
				this.cart.receiver?.phone &&
				this.cart.receiver?.email &&
				this.cart.receiver?.address?.address &&
				this.cart.receiver?.address?.area &&
				this.cart.receiver?.address?.state &&
				this.cart.receiver?.address?.country
			);
		},

		get delivery_date() {
			let prep_time = 0;
			for (const item of app.cart_items) {
				if (item.metadata.prep_time > prep_time) {
					prep_time = item.metadata.prep_time;
				}
			}

			const nextWeek = new Date();
			nextWeek.setDate(nextWeek.getDate() + prep_time);
			return nextWeek;
		},

		get total_order() {
			let total = 0;
			for (const i of app.cart_items) {
				total += i.price * i.quantity;
			}
			return total;
		},

		get delivery_cost() {
			let dc = 0;
			if (this.has_receiver) {
				dc = get_delivery_cost(app.cart_items, this.cart.receiver.address.area);
			}
			return dc;
		},

		get discount() {
			let _discount = 0;
			if (this.coupon) {
				let applies_to = 0;
				if (this.coupon.benefit.applies_to == 'total order') {
					applies_to = this.total_order;
				} else if (this.coupon.benefit.applies_to == 'delivery fee') {
					applies_to = this.has_receiver ? this.delivery_cost : 0;
				}

				if (this.coupon.benefit.value_unit == 'flat') {
					_discount = this.coupon.benefit.value;
				} else if (this.coupon.benefit.value_unit == 'percent') {
					_discount = (applies_to * this.coupon.benefit.value) / 100;
					_discount = Math.round(_discount * 100) / 100;
				}

				_discount = Math.min(_discount, applies_to);
			}
			return _discount;
		},
		get discount_condition_met() {
			let condition_met = true;
			if (this.coupon && this.coupon.benefit.condition > 0) {
				if (this.coupon.benefit.condition_unit == 'total order') {
					condition_met = this.total_order >= this.coupon.benefit.condition;
				} else {
					condition_met = false;
				}
			}

			return condition_met;
		},

		get pay() {
			let sum = this.total_order;
			if (this.has_receiver) {
				sum += Number(this.delivery_cost);
			}
			if (this.coupon && this.discount_condition_met) {
				sum -= this.discount;
			}

			return Math.max(sum, 0);
		}
	});
</script>

<Meta
	title="Cart"
	description="Review your selected items, adjust quantities, and proceed securely to checkout."
/>
<Log entity_type={'page'} />

<Content --content-padding-top="1px">
	<div class="page_title">Cart</div>
	{#if app.cart_items.length}
		<Cart bind:ops></Cart>
		<Receiver bind:ops previous_receivers={data.previous_receivers}></Receiver>
		<Coupons bind:ops></Coupons>

		<div class="terms" id="terms">
			<Checkbox
				value={ops.agree}
				onclick={() => {
					ops.agree = !ops.agree;
					ops.error = {};
				}}
			></Checkbox>
			<span>
				By checking this box, you agree to our
				<Link href="/legal/terms">terms and conditions</Link>
			</span>
		</div>
	{:else}
		<PageNote>
			No item in cart yet
			<div class="icon">
				<Icon icon="cart" size="50" />
			</div>
			<Button icon="shop" href="/shop">Shop now</Button>
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
		display: flex;
		gap: 16px;
		margin-top: 24px;
		font-size: 0.8rem;
		--link-font-size: 0.8rem;
	}
</style>
