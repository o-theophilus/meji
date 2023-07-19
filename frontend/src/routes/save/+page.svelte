<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	export let { items } = data;
	let total_page = 10;

	const unsaved = async (key) => {
		items = items.filter((i) => i.key != key);
	};
</script>

<Meta title="Saved" description="Saved" />

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

<Pagination page_name="save" {total_page} />

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
