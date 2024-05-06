<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';
	import Center from '$lib/center.svelte';
	import Meta from '$lib/meta.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Search from './search.svelte';
	import Log from './log.svelte';
	import Back from '$lib/button/back.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: logs = data.logs;
	$: total_page = data.total_page;
	let { search_query } = data;

	let search;
</script>

<UpdateUrl />
<Meta title="Logs" description="Logs" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Logs
	</Title>
</Center>

<Card>
	<Search bind:this={search} {search_query} />

	{#each logs as log (log.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Log
				{log}
				on:search={(e) => {
					search.set_value(e.detail);
				}}
			/>
		</div>
	{:else}
		<br />
		no item here
	{/each}
	<Pagination {total_page} card />
</Card>

<style>
</style>
