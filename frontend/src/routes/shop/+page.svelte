<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';
	import Center from '$lib/center.svelte';
	import UpdateUrl from '$lib/update_url.svelte';
	import Status from '$lib/status.svelte';
	import Search from '$lib/search.svelte';
	import Tag from './_tags.svelte';
	import View from './view.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import Pagination from '$lib/pagination.svelte';
	import FilterNote from './filter_note.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;
	let { tags } = data;
	let { item_status } = data;
</script>

<UpdateUrl />
<Meta title="Shop" description="Shop" />
<Log entity_type={'page'} />

<Center>
	<br />
	<div class="ctitle">
		Shop
		<div class="line">
			<View />
			<OrderBy {page_name} {order_by} />
		</div>
	</div>
</Center>

<Card>
	{#if $user.permissions.includes('item:add') || $user.permissions.includes('item:edit_status')}
		<Status {page_name} array={item_status} default_value="live">
			{#if $user.permissions.includes('item:add')}
				<Button
					class="primary"
					on:click={() => {
						$module = {
							module: Add
						};
					}}
				>
					<SVG type="add" size="12" />
					Add
				</Button>
			{/if}
		</Status>
		<br />
	{/if}

	<div class="line">
		<Button
			on:click={() => {
				$module = {
					module: Tag,
					tags,
					page_name
				};
			}}
		>
			Tags
		</Button>

		<Search {page_name} />
	</div>
</Card>

<FilterNote {page_name} />

{#if items.length > 0}
	<br />
	<Center>
		<div class="item_area" class:list={$user.setting_item_view == 'list'}>
			{#each items as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Item {item} list={$user.setting_item_view == 'list'} />
				</div>
			{/each}
		</div>
	</Center>
{:else}
	<Card>no item here</Card>
{/if}

<Pagination {page_name} {total_page} />

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
