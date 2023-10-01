<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	// import Search from '$lib/search.svelte';
	import Log from './log.svelte';
	import StatusType from './status_type.svelte';
	import StatusAction from './status_action.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;
	let { page_name } = data;

	let type = '';
	let status = '';

	let actions = {
		item: ['viewed', 'added_photo'],
		order: ['created', 'ordered', 'changed_delivery_date', 'changed_status', 'canceled'],
		voucher: ['created', 'changed_status', 'activated', 'used'],
		advert: ['created', 'added_photo', 'deleted']
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			status = params.get('status');
			type = status.split(':')[0];
		}
	});
</script>

<Meta title="Logs" description="Logs" />

<!-- <Search {page_name} /> -->
<Center>
	<br />
	<b>
		{$page.url.searchParams.has('admin') ? 'All' : 'My'} Log{logs.length > 1 ? 's' : ''}
	</b>
</Center>

<Card>
	<StatusType {page_name} {actions} bind:type bind:status />
	<StatusAction {page_name} {actions} bind:type bind:status />

	<br />

	{#each logs as log (log.key)}
		<Log {log} />
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
