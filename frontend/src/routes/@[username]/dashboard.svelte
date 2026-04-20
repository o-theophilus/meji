<script>
	import { page } from '$app/state';
	import { app, page_state } from '$lib/store.svelte.js';

	import { LinkArrow } from '$lib/button';
	import { Card, Summary, Table } from '$lib/dashboard';
	import { onMount } from 'svelte';

	let dashboard = $state(page.data.dashboard);

	onMount(() => {
		for (let x of dashboard.order_recent) {
			x.id = `#${x.key.substring(0, 8)}`;
			x.total = `₦${Number(x.total).toLocaleString()}`;
			x.href = `/orders/${x.key}`;
		}

		for (let x of dashboard.recently_viewed) {
			x.price = `₦${Number(x.price).toLocaleString()}`;
			x.href = `/${x.slug}`;
		}

		for (let x of dashboard.give_feedback) {
			x.action = 'give feedback';
			x.href = `/${x.slug}`;
			x.href2 = `/${x.slug}/review`;
		}

		for (let x of dashboard.activity_log) {
			x.date = x.date_created; //TODO: format this to 20/04/2026 8:34 pm
		}
	});
</script>

<br />
<br />
<br />
<br />
<br />

<div class="container">
	<div class="two margin">
		<Card>
			<Summary title="Total Orders" data={dashboard.order_count} icon="receipt-text"></Summary>
		</Card>
		<Card>
			<Summary title="Last Order Date" data={dashboard.last_order_date} icon="calendar-days"
			></Summary>
		</Card>
	</div>

	<div class="order_container margin">
		<Card title="RECENT ORDERS">
			<Table data={dashboard.order_recent} columns={['id:href', 'total', 'status']}></Table>
			<LinkArrow href="/orders" --link-font-size="0.7rem">View more</LinkArrow>
		</Card>
	</div>

	<div class="margin two">
		<Card title="Give Feedback">
			<Table data={dashboard.give_feedback} columns={['name:href', 'action:href2']}></Table>
		</Card>

		<Card title="Recently Viewed">
			<Table data={dashboard.recently_viewed} columns={['name:href', 'price']}></Table>
		</Card>
	</div>

	<div class="margin">
		<Card title="Activity Log">
			<Table
				data={dashboard.activity_log}
				columns={['date_created:date', 'action', 'entity_type', 'entity_key']}
			></Table>

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

	/* .four {
		display: grid;
		gap: 16px;
		grid-template-columns: repeat(2, 1fr);

		@container (min-width: 600px) {
			& {
				grid-template-columns: repeat(4, 1fr);
			}
		}
	} */

	.margin {
		margin-top: 16px;
	}
</style>
