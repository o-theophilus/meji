<script>
	import { replaceState } from '$app/navigation';
	import { BackButton, Button } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination, Search } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Add from './_add.svelte';
	import One from './one.svelte';

	let { data } = $props();
	let coupons = $derived(data.coupons);
	let total_page = $derived(data.total_page);
	let { order_by } = data;
	let { _status } = data;
	let searchParams = $state(data.searchParams);
	let defaultParams = $state(data.searchParams);

	const update = (a, b) => {
		coupons = a;
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
<Meta title="All Coupons" />

<Content --content-height="auto">
	<div class="line space">
		<div class="line">
			<BackButton />
			<div class="page_title">
				Coupon{coupons?.length > 1 ? 's' : ''}
			</div>
		</div>

		<div class="line">
			<Dropdown
				icon2="chevron-down"
				list={_status}
				bind:value={searchParams.status}
				onchange={(v) => {
					searchParams.page_no = 1;
					page_state.set({ status: v == defaultParams.status ? '' : v });
				}}
			/>

			{#if app.user.access.includes('coupon:add')}
				<Button icon="plus" extra="outline" onclick={() => module.open(Add, { update })}>Add</Button
				>
			{/if}
		</div>
	</div>

	<Search
		bind:value={searchParams.search}
		ondone={(v) => {
			searchParams.page_no = 1;
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
			page_state.set({ status: v == defaultParams.status ? '' : v });
		}}
	/>
</Content>

<Content --content-padding-top="1px">
	{#each coupons as coupon (coupon.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {coupon} all={searchParams.status == 'all'} />
		</div>
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No coupon found
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
