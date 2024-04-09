<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { user, set_state } from '$lib/store.js';

	import Meta from '$lib/meta.svelte';
	import Log from '$lib/log.svelte';
	import Card from '$lib/card.svelte';
	import Item from '$lib/item/index.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Center from '$lib/center.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import Search from '$lib/search.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	export let data;
	$: items = data.items;
	$: total_page = data.total_page;
	let { page_name } = data;
	let { order_by } = data;

	$: {
		items = items.filter((x) => $user.saves.includes(x.key));
	}

	let search = '';
	let _search = '';
	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('search')) {
			search = params.get('search');
			_search = params.get('search');
		}
	});
	const submit = () => {
		if (_search != search) {
			_search = search;
			set_state(page_name, 'search', search);
		}
	};

	let filter = '';
	$: {
		filter = '';
		if ($page.url.searchParams.has('search')) {
			filter = `Showing result for [${$page.url.searchParams.get('search')}]`;
		}
	}
</script>

<UpdateUrl />
<Meta title="Saved" description="Saved" />
<Log action="viewed" entity_type="save" />

<Center>
	<br />
	<div class="ctitle">
		Saved Item{items.length > 1 ? 's' : ''}
		<div class="line">
			<OrderBy {page_name} {order_by} default_value="latest" />
		</div>
	</div>
</Center>

<Card>
	<div class="line">
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
		<div class="item_area">
			{#each items as item (item.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Item {item} />
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
		border-radius: var(--sp1);

		background-color: var(--cl1_t);
		color: var(--ac1);
		font-size: small;
	}
</style>
