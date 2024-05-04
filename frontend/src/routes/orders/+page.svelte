<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, set_state } from '$lib/store.js';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Status from '$lib/status.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import Order from './order.svelte';
	import Back from '$lib/button/back.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import UpdateUrl from '$lib/update_url.svelte';
	import Search from '$lib/search.svelte';

	export let data;
	$: orders = data.orders;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { order_status } = data;

	let is_admin = false;

	onMount(() => {
		is_admin = $page.url.searchParams.has('admin');
	});
</script>

<UpdateUrl />
<Meta title="Order" description="Order" />
{#key `${$page.url.pathname}${$page.url.search}`}
	<Log entity_type="page" />
{/key}

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Orders
			{#if $user.permissions.includes('order:view')}
				<Toggle
					state_1="Mine"
					state_2="All"
					active={is_admin}
					on:click={() => {
						if (is_admin) {
							set_state('admin', '');
							is_admin = false;
						} else {
							set_state('admin', 'true');
							is_admin = true;
						}
					}}
				/>
			{/if}
		</div>

		<OrderBy {order_by} />
	</div>
</Center>

<Card>
	<Status array={[...order_status, 'all']} default_value="created" />
	<br />
	<Search />
	<br />

	{#each orders as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Order order={x} {is_admin} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</Card>

<style>
</style>
