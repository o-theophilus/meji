<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, page_state, app } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { Content } from '$lib/layout';
	import { Button, Radio, BackButton } from '$lib/button';
	import { Dropdown, Search, Pagination } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Meta, Icon, Log } from '$lib/macro';
	import { Login } from '$lib/auth';
	import One from './one.svelte';
	import Add from './_add.svelte';
	import Control from './one.control.svelte';

	let { data } = $props();
	let { item } = data;
	let reviews = $derived(data.reviews);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let search = $state({ order: 'oldest', search: '', page_no: 1 });

	const update = (a, b) => {
		reviews = a;
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
	title="Review"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-height="auto" --content-background-color="var(--bg2)">
	<div class="line">
		<BackButton href="/{item.slug}" />
		<div class="page_title">Review{reviews.length ? 's' : ''}</div>
	</div>

	<Search
		bind:value={search.search}
		ondone={(v) => {
			search.page_no = 1;
			page_state.set({ search: v });
		}}
	></Search>

	<div class="button">
		{#if app.login}
			<Button icon="message-circle-plus" onclick={() => module.open(Add, { item, update, search })}>
				Add review
			</Button>
		{:else}
			<Button icon="log-in" onclick={() => module.open(Login)}>Login to add review</Button>
		{/if}
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
		bind:value={search.order}
		onchange={(v) => {
			search.page_no = 1;
			v = v == 'oldest' ? '' : v;
			page_state.set({ order: v });
		}}
	/>
</Content>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	{#each reviews as review (review.key)}
		<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {review}>
				{#snippet control()}
					<Control {item} {review} {update} {search}></Control>
				{/snippet}
			</One>
		</div>
	{:else}
		<PageNote>
			<Icon icon="message-circle-off" size="50" />
			No review
		</PageNote>
	{/each}

	<Pagination
		{total_page}
		bind:value={search.page_no}
		ondone={(v) => {
			if (v == 1) v = 0;
			page_state.set({ page_no: v });
		}}
	></Pagination>
</Content>
