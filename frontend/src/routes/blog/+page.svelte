<script>
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content, PageTitle } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Add from './_add.svelte';
	import FilterNote from './filter_note.svelte';
	import One from './one.svelte';
	import Tags from './tags.svelte';

	let { data } = $props();
	let blogs = $derived(data.blogs);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let status = $derived(data.status);
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);
	let pagination = $state();

	const update = (a, b) => {
		blogs = a;
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
	title="Blogs"
	description="Explore stories on style, design, and smart living—curated to help you discover better products and make confident choices on Meji."
/>
{#key page.url}
	<Log entity_type={'page'} />
{/key}

<Content --content-height="auto">
	<PageTitle>
		{#snippet title()}
			Insights, inspiration, and ideas to elevate your everyday.
		{/snippet}
		{#snippet copy()}
			Explore stories on style, design, and smart living—curated to help you discover better
			products and make confident choices on Meji.
		{/snippet}
	</PageTitle>

	<div class="line space">
		<div></div>
		{#if app.user.access.includes('blog.add')}
			<Button
				icon="plus"
				--button-height="32px"
				--button-font-size="0.8rem"
				onclick={() => module.open(Add, { update })}>Add</Button
			>
		{/if}
	</div>

	<Search
		bind:value={search_params.search}
		ondone={(v) => {
			search_params.page_no = 1;
			pagination.reset();
			page_state.set({ search: v });
		}}
	></Search>

	<div class="line space">
		<div class="line">
			{#if app.user.access.includes('item.add')}
				<Dropdown
					--select-height="32px"
					--select-padding-x="8px"
					--select-font-size="0.8rem"
					label="Status: {search_params.status}"
					list={status}
					icon="list-filter"
					icon2="chevron-down"
					bind:value={search_params.status}
					onchange={(v) => {
						search_params.page_no = 1;
						pagination.reset();
						page_state.set({ status: v == default_params.status ? '' : v });
					}}
				/>
			{/if}
			<Tags
				bind:this={tags}
				bind:value={search_params.tag}
				ondone={(v) => {
					search_params.page_no = 1;
					pagination.reset();
					page_state.set({ tag: v });
				}}
			/>
		</div>

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
			search_params.tag = '';
			tags.clear();
			page_state.set({ search: '', tag: '' });
		}}
	/>
</Content>

<Content --content-padding-top="1px" --content-width="1500px">
	{#if blogs.length}
		<section class="items">
			{#each blogs as blog (blog.key)}
				<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
					<One {blog} />
				</div>
			{/each}
		</section>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No post found
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
		margin: 16px 0;
		display: grid;
		gap: 16px;
	}

	@media screen and (min-width: 550px) {
		.items {
			grid-template-columns: repeat(2, 1fr);
		}
	}

	@media screen and (min-width: 850px) {
		.items {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 1200px) {
		.items {
			grid-template-columns: repeat(4, 1fr);
		}
	}
</style>
