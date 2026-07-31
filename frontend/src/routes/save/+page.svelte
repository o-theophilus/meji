<script>
	import { replaceState } from '$app/navigation';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import FilterNote from '../shop/filter_note.svelte';
	import Item from '../shop/item.svelte';

	let { data } = $props();
	let items = $derived(data.items.filter((x) => app.likes.includes(x.key)));
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);
	let pagination = $state();

	const update = (a, b) => {
		items = a;
		total_page = b;
	};

	onMount(() => {
		const sp = page_state.search_params;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(search_params)) {
				if (sp[key]) search_params[key] = sp[key];
			}
		}
	});

	let tags = $state();
</script>

<Meta
	title="Save"
	description="Keep track of your favorite items and come back to them anytime you're ready to shop."
/>
<Log entity_type={'page'} />

<Content --content-height="auto">
	<div class="page_title">Save</div>

	<Search
		bind:value={search_params.search}
		ondone={(v) => {
			search_params.page_no = 1;
			pagination.reset();
			page_state.set({ search: v });
		}}
	></Search>

	<div class="line space">
		<div></div>
		<Dropdown
			--select-height="1"
			--select-padding-x="0"
			--select-font-size="0.8rem"
			--select-background-color="transparent"
			--select-background-color-hover="transparent"
			--select-color="var(--ft2)"
			--select-color-hover="var(--ft1)"
			--select-outline-color="transparent"
			label="Sort: {search_params.order}"
			list={order_by}
			icon="arrow-down-up"
			icon2="chevron-down"
			bind:value={search_params.order}
			onchange={(v) => {
				search_params.page_no = 1;
				pagination.reset();
				page_state.set({ order: v == default_params.order ? '' : v });
			}}
		/>
	</div>

	<FilterNote
		onclick={() => {
			search_params.page_no = 1;
			pagination.reset();
			search_params.search = '';
			page_state.set({ search: '' });
		}}
	/>
</Content>

<Content --content-padding-top="1px" --content-width="1500px">
	{#if items.length}
		<section class="items">
			{#each items as item (item.key)}
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
		bind:this={pagination}
		bind:value={search_params.page_no}
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
		gap: 8px;

		margin: 16px 0;
	}

	@media screen and (min-width: 580px) {
		.items {
			gap: 24px;
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
