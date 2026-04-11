<script>
	import { Button } from '$lib/button';
	import { app, module } from '$lib/store.svelte.js';
	import CancelForm from './status.canceled.svelte';
	import DeliveredForm from './status.delivered.svelte';
	import EnrouteForm from './status.enroute.svelte';
	import ProcessingForm from './status.processing.svelte';
	import ReturnedForm from './status.returned.svelte';
	import ReturningForm from './status.returning.svelte';

	let { order, items, update } = $props();
	let return_time_left = $derived.by(() => {
		let delivered = new Date(order.timeline.delivered);
		if (isNaN(delivered)) return 0;

		delivered = Date.UTC(
			delivered.getUTCFullYear(),
			delivered.getUTCMonth(),
			delivered.getUTCDate()
		);

		return Math.max(0, 7 * 24 * 60 * 60 * 1000 - (Date.now() - delivered));
	});
</script>

<div class="line">
	{#if order.status == 'enroute' && app.user.access.includes('order.status.processing')}
		<Button icon="arrow-left" onclick={() => module.open(ProcessingForm, { order, items, update })}
		></Button>
	{/if}

	{#if order.status == 'created' && app.user.access.includes('order.status.processing')}
		<Button
			icon2="arrow-right"
			onclick={() => module.open(ProcessingForm, { order, items, update })}
		>
			Processing
		</Button>
	{:else if order.status == 'processing' && app.user.access.includes('order.status.enroute')}
		<Button icon2="arrow-right" onclick={() => module.open(EnrouteForm, { order, items, update })}>
			Enroute
		</Button>
	{:else if order.status == 'enroute' && app.user.access.includes('order.status.delivered')}
		<Button
			icon2="arrow-right"
			onclick={() => module.open(DeliveredForm, { order, items, update })}
		>
			Delivered
		</Button>
	{:else if order.status == 'delivered' && app.user.key == order.user_key && return_time_left > 0}
		<Button
			icon="undo-2"
			--button-background-color="darkred"
			--button-background-color-hover="red"
			--button-color-hover="white"
			onclick={() => module.open(ReturningForm, { order, items, update })}
		>
			Return Order ({Math.ceil(return_time_left / (24 * 60 * 60 * 1000))} day{Math.ceil(
				return_time_left / (24 * 60 * 60 * 1000)
			) > 1
				? 's'
				: ''} left)
		</Button>
	{:else if order.status == 'returning' && app.user.access.includes('order.status.returned')}
		<Button
			onclick={() => module.open(ReturnedForm, { order, items, update })}
		>
			Receive Returned Order
		</Button>
	{/if}

	{#if ['created', 'processing', 'enroute'].includes(order.status) && app.user.access.includes('order.status.canceled')}
		<Button
			icon="trash-2"
			--button-background-color="darkred"
			--button-background-color-hover="red"
			--button-color-hover="white"
			onclick={() => module.open(CancelForm, { order, items, update })}
		>
			Cancel Order
		</Button>
	{/if}
</div>
