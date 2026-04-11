<script>
	import { Button, RoundButton } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Datetime, Log, Meta } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Table from './_page.items_table.svelte';
	import Receiver from './_page.receiver.svelte';
	import DateForm from './form.date.svelte';
	import StatusControl from './status.svelte';
	import StatusView from './view_status.svelte';

	let { data } = $props();
	let order = $state(data.order);
	let items = data.items;
	let coupon = data.coupon;

	let discount = $derived.by(() => {
		let applies_to = 0;
		let _discount = 0;
		if (coupon) {
			if (coupon.benefit.applies_to == 'total order') {
				applies_to = order.order_cost;
			} else if (coupon.benefit.applies_to == 'delivery fee') {
				applies_to = order.delivery_cost;
			}

			if (coupon.benefit.value_unit == 'flat') {
				_discount = coupon.benefit.value;
			} else if (coupon.benefit.value_unit == 'percent') {
				_discount = (applies_to * coupon.benefit.value) / 100;
				_discount = Math.round(_discount * 100) / 100;
			}

			_discount = Math.min(_discount, applies_to);
		}
		return _discount;
	});

	const update = (new_order) => {
		order = new_order;
	};
</script>

<Log entity_type={'page'} />
<Meta title="Order" />

<Content --content-padding-top="1px">
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
	<StatusView {order}></StatusView>

	<br />
	<div class="card">
		<Table {items} />
		<br />
		<div class="line space">
			<span class="label bold"> Total order: </span>
			<span class="cost">
				₦{Number(order.order_cost).toLocaleString()}
			</span>
		</div>
		<div class="line space">
			<span class="label bold"> Delivery fee: </span>
			<span class="cost">
				₦{Number(order.delivery_cost).toLocaleString()}
			</span>
		</div>

		<hr class="hr" />

		<div class="line space">
			<span class="label bold"> Discount: </span>
			<span class="cost">
				₦{Number(discount).toLocaleString()}
			</span>
		</div>
		<div class="line space">
			<span class="label bold"> User paid: </span>
			<span class="cost">
				₦{Number(order.payment).toLocaleString()}
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

		{#if order.status == 'created' && app.user.access.includes('order.edit_delivery_date')}
			<br />
			<Button onclick={() => module.open(DateForm, { ...order, update })}>Edit</Button>
		{/if}
	</div>

	<br />

	<StatusControl {order} {items} {update}></StatusControl>
</Content>

<style>
	.page_title_block {
		margin: 24px 0;
	}
	.page_title_block .label {
		text-transform: uppercase;
	}

	.hr {
		margin: 24px 0;
	}

	.card {
		padding: 24px;
		border-radius: 8px;
		background-color: var(--bg);
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
