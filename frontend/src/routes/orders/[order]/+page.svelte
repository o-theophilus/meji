<script>
	import { user, module, portal } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Center from '$lib/center.svelte';
	import SVG from '$lib/svg.svelte';

	import Item from './items.svelte';
	import Eta from './eta.svelte';
	import Receiver from './receiver.svelte';
	import Status from './_status.svelte';
	import Cancel from './_status_cancel.svelte';
	import Form from './eta._form.svelte';

	export let data;
	let { order } = data;
	let date_time = order.delivery_date.split('T');

	$: if ($portal && $portal.type == 'order') {
		order = $portal.data;
		$portal = '';
	}
</script>

<Meta title="Order" description="Order" />

<Center>
	<br />
	<div class="ctitle">Order</div>
</Center>

<Card>
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
			<Receiver {order} />

			<br />

			<Eta {order}>
				{#if order.status == 'created' && $user.roles.includes('admin')}
					<Button
						class="link"
						on:click={() => {
							$module = {
								module: Form,
								key: order.key,
								date: date_time[0],
								time: date_time[1]
							};
						}}
					>
						Edit
					</Button>
				{/if}
			</Eta>
		</div>
	</div>

	{#if !['delivered', 'canceled'].includes(order.status)}
		<br />
		<br />
		<div class="line">
			{#if $user.roles.includes('admin')}
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
		font-weight: 500;
	}

	.upper {
		text-transform: capitalize;
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
