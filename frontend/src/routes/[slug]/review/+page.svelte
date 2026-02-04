<script>
	import { replaceState } from '$app/navigation';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, page_state, app, scroll } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { Content } from '$lib/layout';
	import { Button, Radio, BackButton } from '$lib/button';
	import { Dropdown, Search, Pagination } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Meta, Icon, Log } from '$lib/macro';
	import { Login } from '$lib/auth';
	import RatingSummary from './rating.summary.svelte';
	import Add from './_add.svelte';
	import One from './one.svelte';

	let { data } = $props();
	let { item } = data;
	let reviews = $derived(data.reviews);
	let ratings = $derived(data.ratings);
	let has_purchased = $derived(data.has_purchased);
	let can_review = $derived(data.can_review);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let searchParams = $state(data.searchParams);

	const update = (rat, rev, hp, cr, tp) => {
		reviews = rat;
		ratings = rev;
		has_purchased = hp;
		can_review = cr;
		total_page = tp;
	};

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
	title="Review"
	description="Read honest reviews and ratings from verified customers to help you make confident buying decisions."
/>

<Content --content-height="auto" --content-padding-bottom="0">
	<div class="line">
		<BackButton href="/{item.slug}" />
		<div class="page_title">
			Rating{reviews.length ? 's' : ''} and review{reviews.length ? 's' : ''}
		</div>
	</div>

	<br />

	Ratings and reviews from verified customers who have purchased this item.

	<br />
	<br />

	<RatingSummary bind:ratings></RatingSummary>

	<br />

	<div class="line space">
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
				v = v == 'most relevant ▼' ? '' : v;
				page_state.set({ order: v });
			}}
		/>

		{#if !app.login}
			<Button icon="log-in" onclick={() => module.open(Login)}>Login to add review</Button>
		{:else if !has_purchased}
			<!-- TODO: also restrict users from review at the backend -->
			<Button
				icon="message-circle-plus"
				onclick={() =>
					module.open(Dialogue, {
						status: 200,
						title: 'Purchase to Add review',
						message: 'Purchase to Add review',
						buttons: [
							{
								name: 'Ok',
								icon: 'ok',
								fn: () => {
									module.close();
								}
							}
						]
					})}
			>
				Add review
			</Button>
		{:else if can_review}
			<Button
				icon="message-circle-plus"
				onclick={() => module.open(Add, { item, search: { page_size: 3 }, update })}
			>
				Add review
			</Button>
		{/if}
	</div>
</Content>

<Content>
	{#each reviews as review (review.key)}
		<div class="item" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {item} {review} search={searchParams} {update}></One>
		</div>
	{:else}
		<PageNote>
			<Icon icon="message-circle-off" size="50" />
			No review
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

<style>
	.line {
		align-items: flex-end;
	}

	.item {
		margin-top: 8px;
	}
	.item:first-child {
		margin-top: 0;
	}
</style>
