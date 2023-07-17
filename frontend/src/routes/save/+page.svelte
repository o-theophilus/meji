<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	// import { user } from '$lib/store.js';
	// import { state, page_name } from '$lib/page_state.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	export let { items } = data;

	let total_page = 10;

	// $page_name = 'save';
	// let size = 24;
	// $: start = ($state[$page_name].page_no - 1) * size;
	// $: total_page = Math.ceil($user.saves.length / size);
	// $: items = $user.saves.slice(start, start + size);

	const unsaved = async (key) => {
		items = items.filter((i) => i.key != key);
	};
</script>

<Meta title="Saved" description="Saved" />

<!-- <Pagination {total_page} /> -->

<Card>
	<div class="title">Saved</div>

	<div class="items" class:grid={true}>
		{#each items as item (item.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
				<Item
					{item}
					on:unsaved={() => {
						unsaved(item.key);
					}}
					on:done={(e) => {
						items = e.detail.items;
					}}
				/>
			</div>
		{:else}
			no saved item
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
