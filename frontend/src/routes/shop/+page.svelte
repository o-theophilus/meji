<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { user, module, set_state } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
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

	let tags;
	onMount(async () => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tag`);
		resp = await resp.json();
		if (resp.status == 200) {
			tags = resp.tags;
		}
	});

	let filter = '';
	$: {
		filter = 'Showing result for ';
		if ($page.url.searchParams.has('search') && $page.url.searchParams.has('tag')) {
			filter = `${filter} ${$page.url.searchParams.get(
				'search'
			)} with tags ${$page.url.searchParams.get('tag')}`;
		} else if ($page.url.searchParams.has('search')) {
			filter = `${filter} search ${$page.url.searchParams.get('search')}`;
		} else if ($page.url.searchParams.has('tag')) {
			filter = `${filter} tags ${$page.url.searchParams.get('tag')}`;
		} else {
			filter = '';
		}
	}
</script>

<Meta title="Shop" description="Shop" />
<Log entity_type={'page'} />

<Center>
	<br />
	<div class="ctitle">
		Shop
		<div class="line">
			<View />
			<Sort {page_name} array={sorts} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	{#if $user.permissions.includes('item:add') || $user.permissions.includes('item:edit_status')}
		<Status {page_name} array={status} default_value="live">
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
			disabled={!tags}
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

	{#if filter}
		<br />
		{filter}
	{/if}
</Card>

{#if items.length > 0}
	<br />
	<Center>
		<div class="item_area" class:list={$user.setting_item_view == 'list'}>
			{#each items as item (item.key)}
				<Item {item} list={$user.setting_item_view == 'list'} />
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
