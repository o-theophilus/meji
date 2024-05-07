<script>
	import { user, module, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import Center from '$lib/center.svelte';
	import SVG from '$lib/svg.svelte';
	import Back from '$lib/button/back.svelte';
	import Log from '$lib/log.svelte';
	import Datetime from '$lib/datetime.svelte';

	import Items from './items.svelte';
	import Receiver from '../../cart/delivery.receiver.svelte';
	import Status from './_status.svelte';
	import Cancel from './_status_cancel.svelte';
	import Eta from './_eta.svelte';

	export let data;
	let { items } = data;
	let { order_status } = data;
	let { order } = data;

	$: if ($portal && $portal.type == 'order') {
		order = $portal.data;
		$portal = '';
	}

	$: if (order.delivery_date) {
		order.delivery_date = new Date(order.delivery_date);
	} else {
		let temp = new Date();
		temp.setDate(temp.getDate() + 4);
		temp.setHours(10, 0, 0, 0);
		order.delivery_date = temp;
	}
</script>

<Meta title="Order" description="Order" />
<Log action={'viewed'} entity_key={order.key} entity_type={'order'} />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Order
	</Title>
</Center>

<Card>
	<div class="grid">
		<span> ID: </span>
		<span class="value">
			{order.key.substring(0, 8)}
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
			<Items {order} {items} />
		</div>

		<div class="hr" />

		<div>
			<Receiver {order} />

			<br />

			<span class="bold"> Estimated time of delivery: </span>
			{#if order.status == 'created'}
				<Link
					on:click={() => {
						$module = {
							module: Eta,
							order
						};
					}}
				>
					Edit
				</Link>
			{/if}
			<br />
			To be delivered on or before
			<span class="bold">
				<Datetime datetime={order.delivery_date} type="day" />,
				<Datetime datetime={order.delivery_date} type="date" style="a" />
			</span>. Time:
			<span class="bold">
				<Datetime datetime={order.delivery_date} type="time" style="a" />
			</span>.
		</div>
	</div>

	{#if !['delivered', 'canceled'].includes(order.status)}
		<br />
		<br />
		<div class="row">
			{#if $user.permissions.includes('order:status')}
				<Button
					on:click={() => {
						$module = {
							module: Status,
							order,
							items,
							order_status
						};
					}}
				>
					Change Status
				</Button>
			{/if}

			{#if order.user == $user.key || $user.permissions.includes('order:cancel')}
				<Button
					extra="hover_red"
					on:click={() => {
						$module = {
							module: Cancel,
							order,
							items
						};
					}}
				>
					<SVG icon="close" size="8" />
					Cancel Order
				</Button>
			{/if}
		</div>
	{/if}
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
		font-weight: 700;
	}

	.upper {
		text-transform: capitalize;
	}

	.row {
		display: flex;
		gap: var(--sp1);
	}

	.bold {
		font-weight: 700;
		color: var(--ac1);
	}
</style>
