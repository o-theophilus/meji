<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button/button.svelte';
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
	import ItemPack from '$lib/item_pack.svelte';
	import Title from '$lib/title.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { order_by } = data;
	let { item_status } = data;
</script>

<UpdateUrl />
<Meta title="Shop" description="Purchase items" />
<Log entity_type={'page'} />

<Center>
	<Title>
		Shop
		<svelte:fragment slot="right">
			<View />
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	{#if $user.permissions.includes('item:add') || $user.permissions.includes('item:edit_status')}
		<Status array={item_status} default_value="live">
			{#if $user.permissions.includes('item:add')}
				<Button
					primary
					on:click={() => {
						$module = {
							module: Add
						};
					}}
				>
					<SVG icon="add" size="12" />
					Add
				</Button>
			{/if}
		</Status>
		<br />
	{/if}

	<div class="row">
		<Button
			on:click={() => {
				$module = {
					module: Tag
				};
			}}
		>
			Tags
		</Button>

		<Search />
	</div>
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
	.row {
		display: flex;
		gap: var(--sp1);
	}
</style>
