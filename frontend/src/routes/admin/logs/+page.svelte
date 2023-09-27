<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Log from './log.svelte';
	import StatusType from './status_type.svelte';
	import StatusAction from './status_action.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;

	let page_name = 'log';
	let type = '';
	let action = '';

	let actions = {
		item: ['viewed', 'added_photo'],
		order: ['created', 'ordered', 'changed_delivery_date', 'changed_status', 'canceled'],
		voucher: ['created', 'changed_status', 'activated', 'used'],
		advert: ['created', 'added_photo', 'deleted']
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			action = params.get('status');
			type = action.split(':')[0];
		}
	});
</script>

<Meta title="Logs" description="Logs" />

<StatusType {page_name} {actions} bind:type bind:action />
<StatusAction {page_name} {actions} bind:type bind:action />

<Card>
	<b> Log{logs.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each logs as log}
		<Log {log} />
	{:else}
		no item here
	{/each}
	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
