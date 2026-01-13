<script>
	import { onMount } from 'svelte';

	import { app } from '$lib/store.svelte.js';
	import { Meta, Log } from '$lib/macro';

	import { Content } from '$lib/layout';
	import { Button, RoundButton } from '$lib/button';
	import { Datetime } from '$lib/macro';
	import Receiver from './_receiver.svelte';
	import Table from './_items_table.svelte';

	let { data } = $props();
	let order = data.order;
	let items = data.items;
</script>

<Log entity_type={'page'} />
<Meta
	title="Order"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	<div class="line">
		<RoundButton icon="arrow-left" href="/orders"></RoundButton>
		<div class="page_title">Order: {order.key.substring(0, 8)}</div>
	</div>

	<div class="card">
		<Table {items} />
		<br />
		<div class="line space">
			<span class="label bold"> Total Item Cost: </span>
			<span class="cost">
				₦{order.cost_items.toLocaleString()}
			</span>
		</div>

		<hr class="hr" />

		<span class="label bold">To be delivered to:</span>
		<br /><br />
		<Receiver receiver={order.receiver} />

		<hr class="hr" />

		<span class="label bold"> Delivery Date: </span>
		<span class="label">
			<Datetime datetime={order.delivery_date} type="date_numeric" />
		</span>

		<hr class="hr" />
		<div class="line space">
			<span class="label bold"> Delivery fee: </span>
			<span class="cost">
				₦{order.cost_delivery.toLocaleString()}
			</span>
		</div>
	</div>
</Content>

<style>
	.page_title {
		margin: 24px 0;
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
