<script>
	import { user, loading } from '$lib/store.js';

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
<Pagination {page_name} {total_page} />

<Card>
	<div class="title">
		Shop

		<!-- <View /> -->
	</div>

	<div class="items" class:grid={true}>
		{#each items as item (item.key)}
			<Item {item} view_list={$user.setting.item_view == 'list'} />
		{:else}
			no item here
		{/each}
	</div>
</Card>

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}

	.items {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: 1fr;

		margin-top: var(--sp4);
		color: var(--ac1);
	}
	.grid {
		grid-template-columns: repeat(2, 1fr);
	}
	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
