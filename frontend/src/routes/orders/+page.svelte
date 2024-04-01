<script>
	import { user, set_state } from '$lib/store.js';
	import { page } from '$app/stores';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Status from '$lib/status.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import Order from './order.svelte';
	import Back from '$lib/button.back.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['created', 'processing', 'enroute', 'delivered', 'canceled'];
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
			{$page.url.searchParams.has('admin') && $user.permissions.includes('order:view')
				? 'All'
				: 'My'} Orders
		</div>

		{#if $user.permissions.includes('order:view')}
			<Button
				class={$page.url.searchParams.has('admin') ? 'primary' : 'outline'}
				on:click={() => {
					if ($page.url.searchParams.has('admin')) {
						set_state(page_name, 'admin', '');
					} else {
						set_state(page_name, 'admin', 'true');
					}
				}}
			>
				{$page.url.searchParams.has('admin') ? 'All' : 'My'} Orders
			</Button>
		{/if}
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
</style>
