<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, module, set_state } from '$lib/store.js';

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

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;
	let { tags } = data;
	let { item_status } = data;

	let search = '';
	let _search = '';
	let filter = '';

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}

		set_filter();
	});
	const submit = () => {
		if (_search != search) {
			_search = search;
			set_state(page_name, 'search', search);
		}
	};

	let set_filter = () => {
		let _s = '';
		let _t = '';
		let multiply = false;
		if ($page.url.searchParams.has('search')) {
			_s = $page.url.searchParams.get('search');
			_s = ` for [${_s}]`;
		}
		if ($page.url.searchParams.has('tag')) {
			_t = $page.url.searchParams.get('tag');
			multiply = _t.substring(_t.length - 2, _t.length) == ':x';
			if (multiply) {
				_t = _t.substring(0, _t.length - 2);
			}
			_t = _t.split(',');
			_t = ` with ${_t.length > 1 ? (multiply ? 'all' : 'any') : ''} tag${
				_t.length > 1 && multiply ? 's' : ''
			} [${_t.join(', ')}]`;
		}

		filter = `${_s || _t ? 'Showing result' : ''}${_s}${_t}`;
	};

	$: set_filter();
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
			<OrderBy {page_name} {order_by} default_value="latest" />
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

{#if filter}
	<Center>
		<div class="filter">
			<span>
				{filter}
			</span>

			<Button
				class="round"
				on:click={() => {
					set_state(page_name, 'search', '');
					set_state(page_name, 'tag', '');
				}}
			>
				<SVG type="close" size="8" />
			</Button>
		</div>
	</Center>
{/if}

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

	.filter {
		display: flex;
		gap: var(--sp2);
		justify-content: space-between;
		align-items: center;

		margin-top: var(--sp2);
		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: var(--cl1_t);
		color: var(--ac1);
		font-size: small;
	}
</style>
