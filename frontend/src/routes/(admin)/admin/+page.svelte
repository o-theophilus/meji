<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { LinkArrow } from '$lib/button/';
	import { Dropdown } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Card from './card.svelte';
	import Donut from './chart_h_bar.svelte';
	import LineChart from './chart_line.svelte';
	import Summary from './summary.svelte';
	import Table from './table.svelte';
	let { data } = $props();
	let { filters } = data;
	let searchParams = $state({ ...data.searchParams });
	let defaultParams = $state(data.searchParams);

	let order_recent = $state([]);
	let item_top_purchase = $state([]);
	let top_users = $state([]);

	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}

		for (let x of page.data.order_recent) {
			x.id = `#${x.key.substring(0, 8)}`;
			x.customer = x.name;
			x.total = `₦${Number(x.total).toLocaleString()}`;
			order_recent.push(x);
		}

		for (let x of page.data.item_top_purchase) {
			x.revenue = `₦${Number(x.total).toLocaleString()}`;
			item_top_purchase.push(x);
		}

		for (let x of page.data.top_users) {
			x.spent = `₦${Number(x.spent).toLocaleString()}`;
			top_users.push(x);
		}
	});

	let cartData = [
		{ label: 'Abandoned', count: 3 },
		{ label: 'Checkout', count: 3 }
	];
</script>

<Log entity_type={'page'} />
<Meta title="Admin Dashboard" />

<Content>
	<div class="page_title">Admin Dashboard</div>

	<Dropdown
		--select-height="32px"
		--select-padding-x="8px"
		--select-font-size="0.8rem"
		label="Interval: {searchParams.interval}"
		icon="list-filter"
		icon2="chevron-down"
		list={filters}
		bind:value={searchParams.interval}
		onchange={(v) => {
			page_state.set({ interval: v == defaultParams.interval ? '' : v });
		}}
	/>

	<div class="container">
		<div class="four margin">
			<Card>
				<Summary
					title="Sales {searchParams.interval}"
					data={page.data.order_revenue}
					money
					icon="banknote"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Orders {searchParams.interval}"
					data={page.data.order_count}
					icon="receipt-text"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={page.data.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Item Available"
					data={page.data.item_available}
					icon="box"
					interval={searchParams.interval}
				></Summary>
			</Card>
		</div>

		<div class="margin">
			<Card title="SALES CHART">
				{#key page.data.sales_chart}
					<LineChart data={page.data.sales_chart}></LineChart>
				{/key}
			</Card>
		</div>

		<div class="order_container margin">
			<Card title="RECENT ORDERS">
				<Table data={order_recent} headers={['id', 'customer', 'total', 'status']}></Table>

				<LinkArrow href="/orders" --link-font-size="0.7rem">View more</LinkArrow>
			</Card>
		</div>

		<div class="margin">
			<Card title="ORDERS STATUS">
				<Donut data={page.data.order_summary}></Donut>
			</Card>
		</div>

		<div class="margin">
			<Card title="Low Stock">
				<Table data={page.data.item_low_quantity} headers={['name', 'quantity']}></Table>
			</Card>
		</div>

		<div class="two margin">
			<Card title="TOP PRODUCTS">
				<Table data={item_top_purchase} headers={['name', 'units', 'revenue']}></Table>
			</Card>
			<Card title="TOP Customers">
				<Table data={top_users} headers={['name', 'orders', 'spent']}></Table>
			</Card>
		</div>

		<div class="margin three">
			<Card title="Conversion Rate (50%)">
				<Donut data={cartData}></Donut>
			</Card>

			<Card title="Coupon Usage">
				Display: Columns
				<br />
				<br />
				Count | 3
				<br />
				Value | 3
			</Card>

			<Card title="Traffic / Analytics">
				Display: Columns
				<br />
				<br />
				page | 3
			</Card>
		</div>

		<br />

		<Card title="ACTIVITY FEED">
			Display: Columns
			<br />
			<br />
			New order placed | time
			<br />
			Product updated | time
			<br />
			Customer registered | time
		</Card>
	</div>
</Content>

<style>
	.container {
		container-type: inline-size;
	}

	.two {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(1, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(2, 1fr);
			}
		}
	}

	.three {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(1, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(3, 1fr);
			}
		}
	}

	.four {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(2, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(4, 1fr);
			}
		}
	}

	.margin {
		margin-top: 16px;
	}
</style>
