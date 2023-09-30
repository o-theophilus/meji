<script>
	import { portal, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Button from '$lib/button.svelte';
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

	let status = ['all', 'inactive', 'unused', 'used'];
</script>

<Meta title="Vouchers" description="Vouchers" />

<Center>
	<br />
	<b> Voucher{vouchers.length > 1 ? 's' : ''} </b>
</Center>

<Card>
	<Status {page_name} array={status} default_value="all">
		<Button
			class="small primary"
			on:click={() => {
				$module = {
					module: Add
				};
			}}
		>
			<SVG type="add" size="12" />
			Add
		</Button>
	</Status>

	<br />
	<Search {page_name} />
	<br />

	{#each vouchers as x}
		<Voucher voucher={x} />
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
	b {
		color: var(--ac1);
	}
</style>
