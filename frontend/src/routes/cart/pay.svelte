<script>
	import { user, module } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	import Card from '$lib/card.svelte';
	import Link from '$lib/button/link.svelte';
	import BRound from '$lib/button/round.svelte';
	import Title from '$lib/title.svelte';

	import MakePayment from './pay.make_payment.svelte';
	import Account from './pay._account.svelte';
	import Voucher from '../profile/_voucher.svelte';

	let emit = createEventDispatcher();

	export let cart;
	export let items;
	$: pay = cart.cost_items + cart.cost_delivery - cart.pay_account;
</script>

<Card>
	<Title card>
		<svelte:fragment slot="left">
			<BRound
				icon="angle"
				icon_size="10"
				on:click={() => {
					emit('back');
				}}
			/>
		</svelte:fragment>
		Payment
	</Title>

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

		<Link
			on:click={() => {
				$module = {
					module: Voucher
				};
			}}
		>
			Add Voucher
		</Link>

		{#if $user.account_balance > 0}
			<div class="value">
				<Link
					on:click={() => {
						$module = {
							module: Account,
							cart
						};
					}}
				>
					Edit
				</Link>
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

	<MakePayment {cart} {items} {pay} />
</Card>

<style>
	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
		align-items: center;
	}
	.value {
		font-weight: 700;
		text-align: right;
	}

	.hr {
		border-top: 2px solid var(--ac4);
		padding-top: var(--sp1);
	}
</style>
