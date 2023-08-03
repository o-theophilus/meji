<script>
	import { module } from '$lib/store.js';

	import Voucher from './invoice__voucher.svelte';
	import Account from './invoice__account.svelte';

	export let order;
	export let user;

	let voucher_form = () => {
		$module = {
			module: Voucher
		};
	};
	let account_form = () => {
		$module = {
			module: Account
		};
	};

	let total_items = order.info.total_items + order.info.delivery_fee;
</script>

<section>
	<div class="title">Delivery Fee</div>
	<div class="value">₦{order.info.delivery_fee.toLocaleString()}</div>
</section>
<section>
	<div class="title">Total Cost</div>
	<div class="value">₦{total_items.toLocaleString()}</div>
</section>

<!-- {#if user.acc_balance > 0} -->
<section>
	<div class="title">Acc. Bal ₦(${user.acc_balance.toLocaleString()})</div>
	<div class="value">₦{order.info.account.toLocaleString()}</div>
</section>
<!-- {/if} -->

<section>
	<div class="title">Pay</div>
	<div class="value">₦{(total_items - order.info.account).toLocaleString()}</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp3);
		font-weight: 500;
		justify-content: right;

		text-align: right;
	}

	.value {
		min-width: 3em;
	}

	.u {
		text-decoration: underline;
		cursor: pointer;
	}
</style>
