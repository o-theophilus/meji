<script>
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Search from './search.svelte';
	import Log from './log.svelte';
	import Back from '$lib/button.back.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;
	let { page_name } = data;
	
	let search;
</script>

<Meta title="Logs" description="Logs" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Logs
		</div>
	</div>
</Center>

<Card>
	<Search bind:this={search} {page_name} />

	<br />

	{#each logs as log (log.key)}
		<Log
			{log}
			on:search={(e) => {
				search.set_value(e.detail);
			}}
		/>
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
