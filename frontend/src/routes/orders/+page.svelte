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
	import One from './one.svelte';

	let { data } = $props();

	let orders = $derived(data.orders);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { status } = data;
	let { view } = data;
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);
	let pagination = $state();

	onMount(() => {
		const sp = page_state.search_params;
		if (Object.keys(sp).length) {
			queueMicrotask(() => replaceState(`?${new URLSearchParams(sp)}`));
			for (const key of Object.keys(search_params)) {
				if (sp[key]) search_params[key] = sp[key];
			}
		}
	});
</script>

<Meta title="All Orders" />
<Log entity_type={'page'} />

<Content --content-height="auto">
	<div class="page_title">
		Order{orders?.length > 1 ? 's' : ''}
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
			{#if app.user.access.includes('order.view')}
				<Dropdown
					--select-height="32px"
					--select-padding-x="8px"
					--select-font-size="0.8rem"
					label="View: {search_params.view}"
					icon="list-filter"
					icon2="chevron-down"
					list={view}
					bind:value={search_params.view}
					onchange={(v) => {
						search_params.page_no = 1;
						pagination.reset();
						page_state.set({ view: v == default_params.view ? '' : v });
					}}
				/>
			{/if}

			<Dropdown
				--select-height="32px"
				--select-padding-x="8px"
				--select-font-size="0.8rem"
				label="Status: {search_params.status}"
				icon="list-filter"
				icon2="chevron-down"
				list={status}
				bind:value={search_params.status}
				onchange={(v) => {
					search_params.page_no = 1;
					pagination.reset();
					page_state.set({ status: v == default_params.status ? '' : v });
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
			icon="arrow-down-up"
			icon2="chevron-down"
			list={order_by}
			bind:value={search_params.order}
			onchange={(v) => {
				search_params.page_no = 1;
				pagination.reset();
				page_state.set({ order: v == default_params.order ? '' : v });
			}}
		/>
	</div>
</Content>

<Content --content-padding-top="1px">
	{#each orders as order (order.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {order} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No order found
		</PageNote>
	{/each}

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
