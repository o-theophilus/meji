<script>
	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';

	import Item from './item.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Back from '$lib/button.back.svelte';
	import Status from '$lib/status.svelte';
	import OrderBy from '$lib/order_by.svelte';

	export let data;
	$: adverts = data.adverts;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { spaces } = data;
	let { sizes } = data;
	let { order_by } = data;
</script>

<Meta title="Item Adverts" description="Here are the items with adverts" />

<Center>
	<br />
	<div class="ctitle">
		<div class="ctitle">
			<Back />
			Advert{adverts.length > 1 ? 's' : ''}
		</div>

		<div class="line">
			<OrderBy {page_name} {order_by} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	<Status {page_name} array={['all', ...spaces]} default_value="all" />
	<br />

	{#each adverts as advert}
		<Item {advert} {sizes} />
	{:else}
		no item here
	{/each}

	<Pagination {page_name} {total_page} />
</Card>

<style>
</style>
