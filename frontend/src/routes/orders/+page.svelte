<script>
	import { user, set_state } from '$lib/store.js';
	import { page } from '$app/stores';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Toggle from '$lib/button.toggle.svelte';
	import Status from '$lib/status.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import Order from './order.svelte';
	import Back from '$lib/button.back.svelte';
	import OrderBy from '$lib/order_by.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;

	let status = ['created', 'processing', 'enroute', 'delivered', 'canceled'];

	$: active = $page.url.searchParams.has('admin');
</script>

<Meta title="Order" description="Order" />
{#key `${$page.url.pathname}${$page.url.search}`}
	<Log entity_type="page" />
{/key}

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			{active && $user.permissions.includes('order:view') ? 'All' : 'My'} Orders
			{#if $user.permissions.includes('order:view')}
				<Toggle
					state_1="Mine"
					state_2="All"
					{active}
					on:click={() => {
						if (active) {
							set_state(page_name, 'admin', '');
						} else {
							set_state(page_name, 'admin', 'true');
						}
					}}
				/>
			{/if}
		</div>

		<!-- TODO: what is line in all OrderBy for? -->
		<div class="line">
			<OrderBy {page_name} {order_by} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	<Status {page_name} array={status} default_value="created" />

	<br />

	{#each orders as x}
		<Order order={x} />
	{:else}
		no item here
	{/each}

	<Pagination {total_page} {page_name} />
</Card>

<style>
	/* .line {
		display: flex;
		gap: var(--sp1);
		align-items: center;
	} */
</style>
