<script>
	import { onMount } from 'svelte';

	import { app, module } from '$lib/store.svelte.js';
	import { Meta, Log } from '$lib/macro';

	import { Content } from '$lib/layout';
	import { Button, RoundButton } from '$lib/button';
	import { Datetime } from '$lib/macro';
	import DateForm from './form.date.svelte';
	import StatusForm from './form.status.svelte';
	import CancelForm from './form.cancel.svelte';
	import Receiver from './_receiver.svelte';
	import Table from './_items_table.svelte';
	import StatusView from './status_view.svelte';

	let { data } = $props();
	let order = $state(data.order);

	let items = data.items;
	let status = data._status;

	let move = $derived.by(() => {
		let i = status.indexOf(order.status);
		let next = i == status.length - 2 ? null : status[i + 1];
		let prev = i == 0 ? null : status[i - 1];
		return { prev, next };
	});

	const update = (new_order) => {
		order = new_order;
	};
</script>

<Log entity_type={'page'} />
<Meta
	title="Order"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	<div class="line">
		<RoundButton icon="arrow-left" href="/orders"></RoundButton>
		<div class="page_title_block">
			<div class="page_title">Order</div>
			<div class="label">
				id:
				<span class="bold">
					{order.key.substring(0, 8)}
				</span>
			</div>
		</div>
	</div>

	<div class="label">Status</div>
	<StatusView {status} {order}></StatusView>

	<br />
	<div class="card">
		<Table {items} />
		<br />
		<div class="line space">
			<span class="label bold"> Total Item Cost: </span>
			<span class="cost">
				₦{Number(order.cost_items).toLocaleString()}
			</span>
		</div>

		<hr class="hr" />

		<span class="label bold">To be delivered to:</span>
		<br /><br />
		<Receiver receiver={order.receiver} />

		<hr class="hr" />

		<div class="label bold">Estimated time of delivery:</div>

		<br />

		<div class="label">
			To be delivered on or before
			<span class="bold">
				<Datetime datetime={order.timeline.delivery_date} type="day_full" />
				<Datetime datetime={order.timeline.delivery_date} type="date_numeric" />
			</span>. Time:
			<span class="bold">
				<Datetime datetime={order.timeline.delivery_date} type="time_period" />
			</span>.
		</div>

		{#if order.status == 'created' && app.user.access.includes('order:edit_delivery_date')}
			<br />
			<Button onclick={() => module.open(DateForm, { ...order, update })}>Edit</Button>
		{/if}

		<hr class="hr" />
		<div class="line space">
			<span class="label bold"> Delivery fee: </span>
			<span class="cost">
				₦{Number(order.cost_delivery).toLocaleString()}
			</span>
		</div>
	</div>

	{#if !['delivered', 'canceled'].includes(order.status)}
		<br />
		<div class="line">
			{#if app.user.access.includes('order:edit_status')}
				{#if move.prev}
					<Button
						icon="arrow-left"
						onclick={() => module.open(StatusForm, { order, items, update, status: move.prev })}
					></Button>
				{/if}
				{#if move.next}
					<Button
						icon2="arrow-right"
						onclick={() => module.open(StatusForm, { order, items, update, status: move.next })}
					>
						<span class="caps">
							{move.next}
						</span>
					</Button>
				{/if}
			{/if}
			{#if app.user.access.includes('order:cancel')}
				<Button
					icon="trash-2"
					--button-background-color="darkred"
					--button-background-color-hover="red"
					--button-color-hover="white"
					onclick={() => module.open(CancelForm, { order, items, update, status: 'canceled' })}
				>
					Cancel Order
				</Button>
			{/if}
		</div>
	{/if}
</Content>

<style>
	.page_title_block {
		margin: 24px 0;
	}
	.page_title_block .label {
		text-transform: uppercase;
	}

	.caps {
		text-transform: capitalize;
	}

	.hr {
		margin: 24px 0;
	}

	.card {
		padding: 24px;
		border-radius: 8px;
		background-color: var(--bg1);
	}

	.label {
		font-size: 0.8rem;
	}
	.bold {
		font-weight: 800;
	}
	.cost {
		font-weight: 700;
		font-size: 1.2rem;
		color: var(--ft1);
	}
</style>
