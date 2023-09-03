<script>
	import { user } from '$lib/store.js';
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	export let { items } = data;
	let { total_page } = data;

	// if $user.save changed refresh items
</script>

<Meta title="Saved" description="Saved" />

<Card>
	<b> Saved </b>

	<div class="item_area" class:list={$user.setting.item_view == 'list'}>
		{#each items as item (item.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
				<Item {item} />
			</div>
		{:else}
			no item here
		{/each}
	</div>
</Card>

<Pagination page_name="save" {total_page} />

<style>
</style>
