<script>
	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';

	import Item from './item.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: adverts = data.adverts;
	$: total_page = data.total_page;

	let page_name = 'advert';
</script>

<Meta title="Advert" description="Advert" />

<Center>
	<br />
	<div class="ctitle">Adverts</div>
</Center>

<Card>
	{#each adverts as advert}
		<Item {advert} />
	{:else}
		no item here
	{/each}
</Card>

<Pagination {page_name} {total_page} />

<style>
</style>
