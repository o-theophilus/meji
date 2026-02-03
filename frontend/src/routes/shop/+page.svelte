<script>
	import { replaceState } from '$app/navigation';
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
	import Item from './item.svelte';
	import Add from './_add.svelte';
	import Tags from './tags.svelte';
	import FilterNote from './filter_note.svelte';

	let { data } = $props();
	let items = $derived(data.items);
	let total_page = $derived(data.total_page);
	// PORTFOLIO update on portfolio website
	let searchParams = $state(data.searchParams);
	let { order_by } = data;
	let { _status } = data;

	const update = (a, b) => {
		items = a;
		total_page = b;
	};

	// PORTFOLIO update on portfolio website
	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			setTimeout(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}
	});

	let tags = $state();
</script>

<Log entity_type={'page'} />
<Meta
	title="Shop"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-height="auto">
	<div class="line space">
		<div class="page_title">Shop</div>
		{#if app.user.access.includes('item:add')}
			<div class="line">
				<Radio
					--button-outline-color-hover="var(--ft1)"
					list={_status}
					bind:value={searchParams.status}
					onclick={(v) => {
						searchParams.page_no = 1;
						v = v == 'active' ? '' : v;
						page_state.set({ status: v });
					}}
				></Radio>
				<Button icon="plus" extra="outline" onclick={() => module.open(Add, { update })}>
					Add New Item
				</Button>
			</div>
		{/if}
	</div>

	<div class="line nowrap">
		<Search
			bind:value={searchParams.search}
			ondone={(v) => {
				searchParams.page_no = 1;
				page_state.set({ search: v });
			}}
		></Search>

		<Tags
			bind:this={tags}
			bind:value={searchParams.tag}
			ondone={(v) => {
				searchParams.page_no = 1;
				page_state.set({ tag: v });
			}}
		/>
	</div>

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
		bind:value={searchParams.order}
		onchange={(v) => {
			searchParams.page_no = 1;
			v = v == 'latest' ? '' : v;
			page_state.set({ order: v });
		}}
	/>

	<FilterNote
		onclick={() => {
			searchParams.page_no = 1;
			searchParams.search = '';
			searchParams.tag = '';
			tags.clear();
			page_state.set({ search: '', tag: '' });
		}}
	/>
</Content>

<Content --content-padding-top="1px" --content-width="100%">
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
		bind:value={searchParams.page_no}
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
