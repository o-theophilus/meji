<script>
	import { user, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import PlaceOrder from './pay.place_order.svelte';
	import Account from './pay._account.svelte';
	import Voucher from '../profile/_voucher.svelte';

	export let cart;
	// $: console.log(cart);
</script>

<Card>
	<section class="grid">
		{#if $user.acc_balance > 0}
			<div class="title">Acc. Bal ₦{$user.acc_balance.toLocaleString()}</div>
			<div class="value">
				₦{cart.transaction.account.toLocaleString()}
			</div>
		{/if}

		<Button
			class="link"
			on:click={() => {
				$module = {
					module: Voucher
				};
			}}
		>
			Add Voucher
		</Button>

		{#if $user.acc_balance > 0}
			<Button
				class="link"
				on:click={() => {
					$module = {
						module: Account,
						cart
					};
				}}
			>
				Edit
			</Button>
		{/if}
	</section>

	<br />

	<PlaceOrder {cart} />
</Card>

<style>
	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
	}
	.value {
		font-weight: 500;
	}

	section {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
	}
</style>
