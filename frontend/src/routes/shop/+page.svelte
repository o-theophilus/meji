<script>
	import { onMount } from 'svelte';
	import { user } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';

	import Status_Bar from './status.svelte';
	import Search from '../profile/search.svelte';
	import Tag from './search.tag.svelte';

	import View from './page_view.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let page_name = 'shop';

	let tags = [];
	let show_tags = false;
	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
		resp = await resp.json();
		if (resp.status == 200) {
			tags = resp.tags;
		}
	});
</script>

<Meta title="Shop" description="Shop" />
<Status_Bar {page_name} />
<Search {page_name}>
	<button
		on:click|stopPropagation={() => {
			show_tags = !show_tags;
		}}
	>
		Tags
	</button>

	{#if show_tags}
		<Tag
			{page_name}
			{tags}
			on:close={() => {
				show_tags = false;
			}}
		/>
	{/if}
</Search>

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

	button {
		background: none;
		border: none;
		color: var(--ac1);
		cursor: pointer;

		padding: var(--sp2) var(--sp4);
	}
	button:hover {
		color: var(--cl1);
	}
</style>
