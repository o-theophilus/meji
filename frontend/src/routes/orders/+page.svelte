<script>
	import { replaceState } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { app, page_state } from '$lib/store.svelte.js';

	import { Content } from '$lib/layout';
	import { BackButton, Radio } from '$lib/button';
	import { Pagination, Dropdown, Search } from '$lib/input';
	import { Meta, Log, Icon } from '$lib/macro';
	import { PageNote } from '$lib/info';
	import One from './one.svelte';

	let { data } = $props();

	let orders = $derived(data.orders);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { _status } = data;
	let searchParams = $state(data.searchParams);

	onMount(() => {
		const sp = page_state.searchParams;
		setTimeout(() => replaceState(`?${new URLSearchParams(sp)}`));
		if (Object.keys(sp).length) {
			for (const key of Object.keys(searchParams)) {
				if (sp[key]) searchParams[key] = sp[key];
			}
		}
	});
</script>

<Log entity_type={'page'} />
<Meta title="All Orders" />

<Content>
	<div class="line space">
		<div class="line">
			<BackButton />
			<div class="page_title">
				Order{orders?.length > 1 ? 's' : ''}
			</div>
		</div>

		<div class="line">
			{#if app.user.access.includes('order:view')}
				<Radio
					--button-outline-color-hover="var(--ft1)"
					list={['me', 'all']}
					bind:value={searchParams.view}
					onclick={(v) => {
						searchParams.page_no = 1;
						v = v == 'me' ? '' : v;
						page_state.set({ view: v });
					}}
				></Radio>
			{/if}

			<Dropdown
				icon2="chevron-down"
				list={['all', ..._status]}
				bind:value={searchParams.status}
				onchange={(v) => {
					v = v == 'created' ? '' : v;
					page_state.set({ status: v });
				}}
			/>
		</div>
	</div>

	<Search
		bind:value={searchParams.search}
		ondone={(v) => {
			page_state.set({ search: v });
		}}
	></Search>

	<Dropdown
		--select-height="10"
		--select-padding-x="0"
		--select-font-size="0.8rem"
		--select-background-color="transparent"
		--select-background-color-hover="transparent"
		--select-color="var(--ft2)"
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

	<br />
	<br />

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
		bind:value={searchParams.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
