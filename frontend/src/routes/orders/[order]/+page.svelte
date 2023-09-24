<script>
	import { user, module, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import Item from './items.svelte';
	import Eta from './eta.svelte';
	import Address from './receiver.svelte';
	import Action from './action.svelte';
	import Status from './_status.svelte';
	import Cancel from './_status_cancel.svelte';
	import Voucher from '../../profile/_voucher.svelte';
	import Account from './_account.svelte';

	export let data;
	let { order } = data;
	let { previous_recipients } = data;

	$: if ($portal) {
		order = $portal;
		$portal = '';
	}
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
		<span class="value upper">
			{order.status}
		</span>
	</div>

	<br />
	<br />

	<div class="block">
		<div>
			<Item {order} />
		</div>

		<div class="hr" />

		<div>
			<Address {order} {previous_recipients} />
			<br />
			<Eta {order} />
		</div>
	</div>

	<br />

	{#if order.status == 'pending' && order.user == $user.key}
		<section class="grid">
			{#if $user.acc_balance > 0}
				<div class="title">Acc. Bal ₦{$user.acc_balance.toLocaleString()}</div>
				<div class="value">
					₦{order.info.account.toLocaleString()}
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
							order
						};
					}}
				>
					Edit
				</Button>
			{/if}
		</section>

		<br />

		<Action {order} />
		<br />
	{/if}

	<div class="line">
		{#if !['pending', 'delivered', 'canceled'].includes(order.status) && $user.roles.includes('admin')}
			<Button
				class="small"
				on:click={() => {
					$module = {
						module: Status,
						order
					};
				}}
			>
				Change Order Status
			</Button>
		{/if}
		{#if !['delivered', 'canceled'].includes(order.status)}
			<Button
				class="hover_red small"
				on:click={() => {
					$module = {
						module: Cancel,
						order
					};
				}}
			>
				<SVG type="close" size="10" />
				Cancel Order
			</Button>
		{/if}
	</div>
</Card>

<style>
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp4);

		width: 100%;
	}

	.hr {
		background-color: var(--ac4);
		width: 2px;
		display: none;
	}

	@media screen and (min-width: 800px) {
		.block {
			flex-direction: unset;
		}
		.hr {
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

	.upper {
		text-transform: capitalize;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
