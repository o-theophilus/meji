<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Log from './log.svelte';
	import Status_Bar from './status.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;

	let item = ['view'];
	let order = ['created', 'ordered', 'changed_delivery_date', 'changed_status', 'canceled'];
	let voucher = ['created', 'changed_status', 'activated', 'used'];
	let page_name = 'logs';
	let status = 'all';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('status')) {
			status = params.get('status');
		}
	});
</script>

<Meta title="Logs" description="Logs" />
<Status_Bar {page_name} bind:status actions={['all']} />
<Status_Bar {page_name} bind:status actions={item} type="item" />
<Status_Bar {page_name} bind:status actions={order} type="order" />
<Status_Bar {page_name} bind:status actions={voucher} type="voucher" />

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
