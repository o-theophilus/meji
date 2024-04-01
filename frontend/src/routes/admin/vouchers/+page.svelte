<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module, set_state, portal, user } from '$lib/store.js';

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

	export let data;
	$: vouchers = data.vouchers;
	$: total_page = data.total_page;
	let { page_name } = data;

	$: if ($portal && $portal.type == 'voucher') {
		vouchers = $portal.data;
		$portal = '';
	}

	let status = ['all', 'inactive', 'active', 'used', 'expired'];

	let search = '';
	let _search = '';
	const submit = () => {
		if (_search != search) {
			_search = `${search}`;
			set_state(page_name, 'search', search);
		}
	};
	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}
	});
</script>

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
	</div>
</Center>

<Card>
	<Status {page_name} array={status} default_value="all">
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
	<div class="line">
		<Search
			bind:search
			on:ok={() => {
				submit();
			}}
			on:clear={() => {
				search = '';
				submit();
			}}
		/>
		<Button class="primary" on:click={submit} disabled={search == _search}>Search</Button>
	</div>
	<br />

	{#each vouchers as x}
		<Voucher voucher={x} />
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
