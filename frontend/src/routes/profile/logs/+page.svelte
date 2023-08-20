<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Log from './log.svelte';
	import Status_Bar from './status.svelte';

	export let data;
	$: logs = data.logs;
</script>

<Meta title="Logs" description="Logs" />
<Status_Bar page_name="log" />

<Card>
	<b> Log{logs.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each logs as log}
		<Log {log} />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
