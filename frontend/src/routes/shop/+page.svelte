<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, module, set_state } from '$lib/store.js';

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
	import Sort from '$lib/sort.svelte';
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

	let search = '';
	let _search = '';
	const submit = () => {
		if (_search != search) {
			_search = `${search}`;
			set_state(page_name, 'search', search);
		}
	};
	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}
	});
</script>

<Meta title="Shop" description="Shop" />

<Center>
	<br />
	<div class="ctitle">
		Shop
		<div class="line">
			<View class="outline" />
			<Sort {page_name} array={sorts} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	{#if $user.roles.includes('admin')}
		<Status {page_name} array={status} default_value="live">
			{#if $user.roles.includes('item:add')}
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
			{/if}
		</Status>
		<br />
	{/if}

	<div class="line">
		<Tag {page_name} />
		<Search
			bind:search
			on:ok={() => {
				submit();
			}}
			on:clear={() => {
				search = '';
				submit();
			}}
		/>
		<Button class="primary" on:click={submit} disabled={search == _search}>Search</Button>
	</div>
</Card>

{#if items.length > 0}
	<br />
	<Center>
		<div class="item_area" class:list={$user.setting.item_view == 'list'}>
			{#each items as item (item.key)}
				<Item {item} list={$user.setting.item_view == 'list'} />
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
