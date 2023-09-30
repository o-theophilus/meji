<script>
	import { portal, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Status from '$lib/status.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';

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
<Status {page_name} {status} default_value="all">
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

<Card>
	<b> Voucher{vouchers.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each vouchers as x}
		{x.date}
		<br />
		{x.status}
		<br />
		<a href="/admin/vouchers/{x.key}">
			{x.key}
		</a>
		<br />
		{x.value}
		<br />

		<br />
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
