<script>
	import { user, module, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Item from './items.svelte';
	import Eta from './eta.svelte';
	import Address from './receiver.svelte';
	import Action from './action.svelte';
	import Status from './status.svelte';
	import Voucher from '../../profile/_voucher.svelte';
	import Account from './_account.svelte';

	export let data;
	let { order } = data;
	let { previous_recipients } = data;

	$: if ($portal) {
		order = $portal;
		$portal = '';
	}
	let mine = order.user_key == $user.key;
</script>

<Meta title="Order" description="Order" />

<Card>
	<b> Order</b>
	<br />
	<br />

	<div class="grid">
		<span> ID: </span>
		<span class="value">
			{order.key}
		</span>
		<span> Status: </span>

		{#if order.status != 'pending' && $user.roles.includes('admin')}
			<Status {order} />
		{:else}
			<span class="value">
				{order.status}
			</span>
		{/if}
	</div>
	<br />
	<br />

	<div class="block">
		<div>
			<Item {order} />
		</div>

		<div class="line" />

		<div>
			<Eta {order} />
			<br />
			<Address {order} {previous_recipients} />
		</div>
	</div>

	{#if order.status == 'pending'}
		<br />

		<section class="grid">
			<div class="title">Total Cost</div>
			<div class="value">
				₦{(order.info.total_items + order.info.delivery_fee).toLocaleString()}
			</div>

			{#if $user.acc_balance > 0}
				<div class="title">Acc. Bal ₦{$user.acc_balance.toLocaleString()}</div>
				<div class="value">
					₦{order.info.account.toLocaleString()}
				</div>
			{/if}
			<Button
				class="link"
				name="Add Voucher"
				on:click={() => {
					$module = {
						module: Voucher
					};
				}}
			/>
			{#if $user.acc_balance > 0}
				<Button
					class="link"
					name="Add Amount"
					on:click={() => {
						$module = {
							module: Account,
							order
						};
					}}
				/>
			{/if}
		</section>

		<br />

		<Action {order} />
	{/if}
</Card>

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp4);

		width: 100%;
	}

	.line {
		background-color: var(--ac4);
		width: 2px;
		display: none;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
		.line {
			display: block;
		}
	}

	.grid {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
	}
	.value {
		color: var(--ac2);
		font-weight: 500;
	}

	section {
		display: grid;
		gap: 0 var(--sp3);
		grid-template-columns: max-content max-content;
	}
</style>
