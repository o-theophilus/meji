<script>
	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Status_Bar from './status.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;
</script>

<Meta title="Logs" description="Logs" />
<Status_Bar page_name="log" />

<Card>
	<b> Log{logs.length > 1 ? 's' : ''} </b>
	<br />
	<br />
	{#each logs as log}
		{log.date}
		<br />
		<a href="/logs/{log.key}">
			{log.action}
		</a>:
		<a href="/{log.entity.slug}">
			{log.entity.name}
		</a>

		<br />
		status: {log.status}
		{#if log.misc}
			<br />
			misc: {log.misc}
		{/if}
		<br />
		<br />
	{:else}
		no item here
	{/each}
</Card>

<style>
</style>
