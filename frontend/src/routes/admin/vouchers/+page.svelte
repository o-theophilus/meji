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
	import Button from '$lib/button/button.svelte';
	import Back from '$lib/button/back.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';
	import Voucher from './voucher.svelte';
	import Center from '$lib/center.svelte';
	import Search from '$lib/search.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import UpdateUrl from '$lib/update_url.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	$: vouchers = data.vouchers;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { voucher_status } = data;

	$: if ($portal && $portal.type == 'voucher') {
		vouchers = $portal.data;
		$portal = '';
	}
</script>

<UpdateUrl />
<Meta title="All Vouchers" />
{#key `${$page.url.pathname}${$page.url.search}`}
	<Log entity_type="page" />
{/key}

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>

		Voucher{vouchers.length > 1 ? 's' : ''}

		<svelte:fragment slot="right">
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<Status array={['all', ...voucher_status]} default_value="all">
		{#if $user.permissions.includes('voucher:add')}
			<Button
				primary
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			>
				<SVG icon="add" size="12" />
				Add
			</Button>
		{/if}
	</Status>
	<br />
	<Search />

	{#each vouchers as x (x.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Voucher voucher={x} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} card />
</Card>

<style>
</style>
