<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { page } from '$app/state';

	import { Content } from '$lib/layout';
	import { Button, Radio } from '$lib/button';
	import { Dropdown, Search, Pagination } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Meta, Icon, Log } from '$lib/macro';

	import Item from '../shop/item.svelte';
	import FilterNote from '../shop/filter_note.svelte';

	let { data } = $props();
	let items = $derived(data.items.filter((x) => app.likes.includes(x.key)));

	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let search = $state({ order: 'latest', search: '', page_no: 1 });

	const update = (a, b) => {
		items = a;
		total_page = b;
	};

	onMount(() => {
		if (page_state.searchParams.order) {
			search.order = page_state.searchParams.order;
		}
		if (page_state.searchParams.search) {
			search.search = page_state.searchParams.search;
		}
		if (page_state.searchParams.page_no) {
			search.page_no = page_state.searchParams.page_no;
		}

		page.url.search = new URLSearchParams(page_state.searchParams);
		window.history.replaceState(history.state, '', page.url.href);
	});

	let tags = $state();
</script>

<Log entity_type={'page'} />
<Meta
	title="Save"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-height="auto">
	<div class="page_title">Save</div>

	<Search
		bind:value={search.search}
		ondone={(v) => {
			search.page_no = 1;
			page_state.set({ search: v });
		}}
	></Search>

	<Dropdown
		--select-height="10"
		--select-padding-x="0"
		--select-font-size="0.8rem"
		--select-background-color="transparent"
		--select-background-color-hover="transparent"
		--select-color-hover="var(--ft1)"
		--select-outline-color="transparent"
		list={order_by}
		icon="arrow-down-narrow-wide"
		icon2="chevron-down"
		bind:value={search.order}
		onchange={(v) => {
			search.page_no = 1;
			v = v == 'latest' ? '' : v;
			page_state.set({ order: v });
		}}
	/>

	<FilterNote
		onclick={() => {
			search.page_no = 1;
			search.search = '';
			page_state.set({ search: '' });
		}}
	/>
</Content>

<Content --content-padding-top="1px" --content-width="1500px">
	{#if items.length}
		<section class="items">
			{#each items as item (item.key)}
				<!-- {#if app.likes.includes(item.key)}
				{/if} -->
				<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<Item {item} />
				</div>
			{/each}
		</section>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No item found
		</PageNote>
	{/if}

	<Pagination
		{total_page}
		bind:value={search.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>

<style>
	.items {
		display: grid;
		grid-template-columns: repeat(2, 1fr);

		justify-content: center;
		flex-wrap: wrap;
		gap: 32px 16px;

		margin: var(--sp2) 0;
	}

	@media screen and (min-width: 580px) {
		.items {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 940px) {
		.items {
			display: flex;
		}
	}

	.items div {
		width: 100%;
		max-width: 280px;
	}
</style>
