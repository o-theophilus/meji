<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Center from '$lib/center.svelte';

	import Item from './item.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Back from '$lib/button/back.svelte';
	import Status from '$lib/status.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import UpdateUrl from '$lib/update_url.svelte';
	import Search from '$lib/search.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	$: adverts = data.adverts;
	$: total_page = data.total_page;
	let { spaces } = data;
	let { sizes } = data;
	let { order_by } = data;
</script>

<UpdateUrl />
<Meta title="Item Adverts" description="Here are the items with adverts" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Advert{adverts.length > 1 ? 's' : ''}
		<svelte:fragment slot="right">
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<Status array={['all', ...spaces]} default_value="all" />
	<br />
	<Search />

	{#each adverts as advert, i (`${advert.key}_${i}`)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<Item {advert} {sizes} />
		</div>
	{:else}
		no item here
	{/each}

	<Pagination {total_page} />
</Card>

<style>
</style>
