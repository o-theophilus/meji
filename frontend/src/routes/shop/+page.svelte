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

	import View from './page_view.svelte';
	import Pagination from '$lib/pagination.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;

	let status = ['live', 'draft', 'delete'];
</script>

<Meta title="Shop" description="Shop" />

<Center>
	<br />
	<div class="title">
		<b> Shop </b>
		<View {page_name} />
	</div>
</Center>

<Card>
	{#if $user.roles.includes('admin')}
		<Status {page_name} {status} default_value="live">
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
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);
		color: var(--ac1);
	}
</style>
