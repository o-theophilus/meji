<script>
	import { page } from '$app/stores';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, portal, user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Button from '$lib/button.svelte';
	import Back from '$lib/button.back.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';
	import Voucher from './voucher.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: vouchers = data.vouchers;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;
	let { voucher_status } = data;

	$: if ($portal && $portal.type == 'voucher') {
		vouchers = $portal.data;
		$portal = '';
	}
</script>

<UpdateUrl />
<Meta title="All Vouchers" description="Vouchers" />
{#key `${$page.url.pathname}${$page.url.search}`}
	<Log entity_type="page" />
{/key}

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Voucher{vouchers.length > 1 ? 's' : ''}
		</div>
		<div class="line">
			<OrderBy {page_name} {order_by} />
		</div>
	</div>
</Center>

<Card>
	<Status {page_name} array={['all', ...voucher_status]} default_value="all">
		{#if $user.permissions.includes('voucher:add')}
			<Button
				class="primary"
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			>
				<SVG type="add" size="12" />
				Add
			</Button>
		{/if}
	</Status>
	<br />
	<Search {page_name} />
	<br />

	{#each vouchers as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Voucher voucher={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
