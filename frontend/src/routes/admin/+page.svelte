<script>
	import { replaceState } from '$app/navigation';
	import { LinkArrow } from '$lib/button/';
	import { Activity, Card, Doughnut, LineChart, Summary, Table } from '$lib/dashboard';
	import { Dropdown } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Log, Meta } from '$lib/macro';
	import { app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';

	let { data } = $props();
	let dashboard = $state(data);

	let { filters } = data;
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);

	let conversion_rate = $state(0);

	onMount(() => {
		const sp = page_state.search_params;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(search_params)) {
				if (sp[key]) search_params[key] = sp[key];
			}
		}

		for (let x of dashboard.order_recent) {
			x.id = `#${x.key.substring(0, 8)}`;
			x.href = `/orders/${x.key}`;
			x.customer = x.name;
			x.href2 = `/@${x.username}`;
			x.total = `₦${Number(x.payment).toLocaleString()}`;
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

		let count = 0;
		let total = 0;
		for (let x of dashboard.conversion_rate) {
			if (x.label == 'cart') {
				total += x.count;
			} else if (x.label == 'checkout') {
				count += x.count;
				total += x.count;
			}
		}
		conversion_rate = Math.round((count * 100) / total);
	});
</script>

<Meta title="Admin Dashboard" />
<Log entity_type={'page'} />

<Content>
	<div class="page_title">Admin Dashboard</div>

	<Dropdown
		--select-height="32px"
		--select-padding-x="8px"
		--select-font-size="0.8rem"
		label="Interval: {search_params.interval}"
		icon="list-filter"
		icon2="chevron-down"
		list={filters}
		bind:value={search_params.interval}
		onchange={(v) => {
			page_state.set({ interval: v == default_params.interval ? '' : v });
		}}
	/>

	<div class="container">
		<div class="four margin">
			<Card>
				<Summary
					title="Sales {search_params.interval}"
					data={dashboard.order_revenue}
					money
					icon="banknote"
					interval={search_params.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Orders {search_params.interval}"
					data={dashboard.order_count}
					icon="receipt-text"
					interval={search_params.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="New Users {search_params.interval}"
					data={dashboard.new_users}
					icon="User"
					interval={search_params.interval}
				></Summary>
			</Card>
			<Card>
				<Summary
					title="Item Available"
					data={dashboard.item_available}
					icon="box"
					interval={search_params.interval}
				></Summary>
			</Card>
		</div>

		<div class="margin">
			<Card title="Sales Chart">
				{#key dashboard.sales_chart}
					<LineChart data={dashboard.sales_chart}></LineChart>
				{/key}
			</Card>
		</div>

		<div class="two margin">
			<Card title="Recent Orders">
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
			<Card title="Orders Status">
				<Doughnut data={dashboard.order_summary}></Doughnut>
			</Card>
		</div>

		<div class="two margin">
			<Card title="Top Products">
				<Table data={dashboard.item_top_purchase} columns={['name', 'units', 'revenue']}></Table>
			</Card>
			<Card title="Top Customers">
				<Table data={dashboard.top_users} columns={['name:href', 'orders', 'spent']}></Table>
			</Card>
		</div>

		<div class="margin three">
			<Card title="Conversion Rate ({conversion_rate}%)">
				<Doughnut data={dashboard.conversion_rate} colors={['#ef4444', '#22c55e']}></Doughnut>
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

		<div class="margin">
			<Card title="Activity Log">
				<Activity data={dashboard.activity_log}></Activity>

				{#if app.user.access.includes('log.view')}
					<LinkArrow
						--link-font-size="0.7rem"
						onclick={() => page_state.goto('log', { u_search: app.user.key })}
					>
						View Logs
					</LinkArrow>
				{/if}
			</Card>
		</div>
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
