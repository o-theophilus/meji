<script>
	import { user } from '$lib/store.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { invalidate } from '$app/navigation';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;
</script>

<Meta title="Saved" description="Saved" />

<Center>
	<br />
	<div class="ctitle">Saved Items</div>
</Center>

{#if items.length > 0}
	<br />
	<Center>
		<div class="item_area">
			{#each items as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Item
						{item}
						on:save_start={() => {
							if (!$user.saves.includes(item.key)) {
								items = items.filter((i) => i.key != item.key);
							}
						}}
						on:save_end={() => {
							invalidate(() => true);
						}}
					/>
				</div>
			{/each}
		</div>
	</Center>
{:else}
	<Card>no item here</Card>
{/if}

<Pagination {page_name} {total_page} />

<style>
</style>
                                                                                               