<script>
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';

	import Status_Bar from './status.svelte';
	import Search from './search.svelte';
	import View from './page_view.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: tags = data.tags;
	$: items = data.items;
	$: total_page = data.total_page;

	let page_name = 'shop';
</script>

<Meta title="Shop" description="Shop" />
<Status_Bar {page_name} />
<Search {page_name} {tags} />

<Card>
	<div class="title">
		<b> Shop </b>
		<View {page_name} />
	</div>

	<div class="item_area" class:list={$user.setting.item_view == 'list'}>
		{#each items as item (item.key)}
			<Item {item} />
		{:else}
			no item here
		{/each}
	</div>
</Card>

<Pagination {page_name} {total_page} />

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);
	}
</style>
