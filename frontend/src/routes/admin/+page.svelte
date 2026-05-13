<script>
	import { replaceState } from '$app/navigation';
	import { LinkArrow } from '$lib/button/';
	import { Card, Doughnut, LineChart, Summary, Table } from '$lib/dashboard';
	import { Dropdown } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	let { data } = $props();
	let dashboard = $state(data);

	let { filters } = data;
	let searchParams = $state({ ...data.searchParams });
	let defaultParams = $state(data.searchParams);

	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}

		for (let x of dashboard.order_recent) {
			x.id = `#${x.key.substring(0, 8)}`;
			x.href = `/orders/${x.key}`;
			x.customer = x.name;
			x.href2 = `/@${x.username}`;
			x.total = `₦${Number(x.total).toLocaleString()}`;
		}

		for (let x of dashboard.item_low_quantity) {
			x.href = `/${x.slug}`;
		}

		for (let x of dashboard.top_users) {
			x.href = `/@${x.username}`;
		}

		for (let x of dashboard.item_top_purchase) {
			x.revenue = `₦${Number(x.total).toLocaleString()}`;
		}

		for (let x of dashboard.top_users) {
			x.spent = `₦${Number(x.spent).toLocaleString()}`;
		}
	});

	let cartData = [
		{ label: 'Abandoned', count: 3 },
		{ label: 'Checkout', count: 3 }
	];
</script>

<Meta title="Admin Dashboard" />
<Log entity_type={'page'} />

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
					data={dashboard.order_revenue}
					money
					icon="banknote"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Orders {searchParams.interval}"
					data={dashboard.order_count}
					icon="receipt-text"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {searchParams.interval}"
					data={dashboard.new_users}
					icon="User"
					interval={searchParams.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Item Available"
					data={dashboard.item_available}
					icon="box"
					interval={searchParams.interval}
				></Summary>
			</Card>
		</div>

		<div class="margin">
			<Card title="SALES CHART">
				{#key dashboard.sales_chart}
					<LineChart data={dashboard.sales_chart}></LineChart>
				{/key}
			</Card>
		</div>

		<div class="two margin">
			<Card title="RECENT ORDERS">
				<Table
					data={dashboard.order_recent}
					columns={['id:href', 'customer:href2', 'total', 'status']}
				></Table>

				<LinkArrow href="/orders" --link-font-size="0.7rem">View more</LinkArrow>
			</Card>

			<Card title="Low Stock">
				<Table data={dashboard.item_low_quantity} columns={['name:href', 'quantity']}></Table>
			</Card>
		</div>

		<div class="margin">
			<Card title="ORDERS STATUS">
				<Doughnut data={dashboard.order_summary}></Doughnut>
			</Card>
		</div>

		<div class="two margin">
			<Card title="TOP PRODUCTS">
				<Table data={dashboard.item_top_purchase} columns={['name', 'units', 'revenue']}></Table>
			</Card>
			<Card title="TOP Customers">
				<Table data={dashboard.top_users} columns={['name:href', 'orders', 'spent']}></Table>
			</Card>
		</div>

		<div class="margin three">
			<Card title="Conversion Rate (50%)">
				<Doughnut data={cartData}></Doughnut>
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
