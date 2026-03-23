<script>
	import { Content, PageTitle } from '$lib/layout';

	import { replaceState } from '$app/navigation';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Icon, Log, Meta } from '$lib/macro';
	import { page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Item from '../shop/item.svelte';

	let { data } = $props();
	let items = $derived(data.items);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let searchParams = $state({ ...data.searchParams });
	let defaultParams = $state(data.searchParams);

	const update = (a, b) => {
		items = a;
		total_page = b;
	};

	onMount(() => {
		const sp = page_state.searchParams;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}
	});
</script>

<Log entity_type={'page'} />
<Meta title="3D Hub" description="A collection of our 3D assets." />

<PageTitle>
	{#snippet title()}
		3D Hub
	{/snippet}
	{#snippet copy()}
		A collection of our 3D assets.
	{/snippet}
</PageTitle>

<Content --content-height="auto">
	<div class="page_title">Save</div>

	<Search
		bind:value={searchParams.search}
		ondone={(v) => {
			searchParams.page_no = 1;
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
			label="Sort: {searchParams.order}"
			list={order_by}
			icon="arrow-down-up"
			icon2="chevron-down"
			bind:value={searchParams.order}
			onchange={(v) => {
				searchParams.page_no = 1;
				page_state.set({ order: v == defaultParams.order ? '' : v });
			}}
		/>
	</div>
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
		bind:value={searchParams.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
