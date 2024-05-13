<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import Search from '$lib/search.svelte';
	import UpdateUrl from '$lib/update_url.svelte';
	import FilterNote from '../shop/filter_note.svelte';
	import ItemPack from '$lib/item_pack.svelte';
	import View from '../shop/view.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { order_by } = data;

	$: {
		items = items.filter((x) => $user.saves.includes(x.key));
	}
</script>

<UpdateUrl />
<Meta title="Saved" description="Items y0u may be interested in" />
<Log action="viewed" entity_type="save" />

<Center>
	<Title>
		Saved Item{items.length > 1 ? 's' : ''}
		<svelte:fragment slot="right">
			<View />
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<Search />
</Card>

<FilterNote />

{#if items.length > 0}
	<Center>
		<ItemPack let:style style={$user.setting_item_view}>
			{#each items as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Item {item} {style} />
				</div>
			{/each}
		</ItemPack>
	</Center>
{:else}
	<Card>no item here</Card>
{/if}

<Pagination {total_page} />

<style>
</style>
