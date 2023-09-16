<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Log from './log.svelte';
	import Status_Bar from './status.svelte';

	let page_name = 'logs';
	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;
</script>

<Meta title="Logs" description="Logs" />
<Status_Bar {page_name} />

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
