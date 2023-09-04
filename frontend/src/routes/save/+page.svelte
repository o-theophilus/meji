<script>
	import { user } from '$lib/store.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { invalidate } from '$app/navigation';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
</script>

<Meta title="Saved" description="Saved" />

<Card>
	<b> Saved </b>

	<div class="item_area" class:list={$user.setting.item_view == 'list'}>
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
		{:else}
			no item here
		{/each}
	</div>
</Card>

<Pagination page_name="save" {total_page} />

<style>
</style>
