<script>
	import { user, module } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import MakePayment from './pay.make_payment.svelte';
	import Account from './pay._account.svelte';
	import Voucher from '../profile/_voucher.svelte';

	let emit = createEventDispatcher();

	export let cart;
	$: pay = cart.cost_items + cart.cost_delivery - cart.pay_account;
</script>

<Card>
	<div class="ctitle">
		<div class="ctitle">
			<Button
				class="round"
				on:click={() => {
					emit('back');
				}}
			>
				<SVG type="angle" size="10" />
			</Button>Payment
		</div>
	</div>

	<br />
	<br />

	<div class="grid">
		<div class="title">Total Item</div>
		<div class="value">
			₦{cart.cost_items.toLocaleString()}
		</div>
		<div class="title">Delivery Fee</div>
		<div class="value">
			₦{cart.cost_delivery.toLocaleString()}
		</div>

		<span>&nbsp;</span>
		<span>&nbsp;</span>

		{#if $user.account_balance > 0}
			<div class="title">
				Acc. Bal ₦{$user.account_balance.toLocaleString()}
			</div>
			<div class="value">
				{#if cart.pay_account > 0}
					-
				{/if}

				₦{cart.pay_account.toLocaleString()}
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

		{#if $user.account_balance > 0}
			<div class="value">
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
			</div>
		{:else}
			<span />
		{/if}

		{#if pay > 0}
			<span>&nbsp;</span>
			<span>&nbsp;</span>

			<div class="title">Pay</div>
			<div class="value hr">
				₦{pay.toLocaleString()}
			</div>
		{/if}
	</div>

	<br />
	<br />

	<MakePayment {cart} {pay} />
</Card>

<style>
	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
		align-items: center;
	}
	.value {
		font-weight: 500;
		text-align: right;
	}

	.hr {
		border-top: 2px solid var(--ac4);
		padding-top: var(--sp1);
	}
</style>
