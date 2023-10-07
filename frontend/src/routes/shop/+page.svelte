<script>
	import { user, module } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import Add from './_add.svelte';
	import Center from '$lib/center.svelte';

	import Status from '$lib/status.svelte';
	import Search from '$lib/search.svelte';
	import Tag from './_tag.svelte';

	import View from './view.svelte';
	import Sort from '../../lib/sort.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['live', 'draft', 'delete'];
	let sorts = [
		'latest',
		'oldest',
		'name (a-z)',
		'name (z-a)',
		'cheap',
		'expensive',
		'discount',
		'rating'
	];
</script>

<Meta title="Shop" description="Shop" />

<Center>
	<br />
	<div class="ctitle">
		Shop
		<div class="line">
			<View {page_name} />
			<Sort {page_name} array={sorts} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	{#if $user.roles.includes('admin')}
		<Status {page_name} array={status} default_value="live">
			<Button
				class="small primary"
				on:click={() => {
					$module = {
						module: Add
					};
				}}
			>
				<SVG type="add" size="12" />
				Add
			</Button>
		</Status>
		<br />
	{/if}

	<Search {page_name}>
		<Tag {page_name} />
	</Search>

	<br />

	<div class="item_area" class:list={$user.setting.item_view == 'list'}>
		{#each items as item (item.key)}
			<Item {item} />
		{:else}
			no item here
		{/each}
	</div>

	<Pagination {page_name} {total_page} />
</Card>

<style>
	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>
