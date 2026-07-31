<script>
	import { replaceState } from '$app/navigation';
	import { Login } from '$lib/auth';
	import { BackButton, Button } from '$lib/button';
	import { Dialogue, PageNote } from '$lib/info';
	import { Dropdown, Pagination } from '$lib/input';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Add from './_add.svelte';
	import One from './one.svelte';
	import RatingSummary from './rating.summary.svelte';

	let { data } = $props();
	let { item } = data;
	let comments = $derived(data.comments);
	let ratings = $derived(data.ratings);
	let has_purchased = $derived(data.has_purchased);
	let can_comment = $derived(data.can_comment);
	let total_page = $derived(data.total_page);
	let order_by = $derived(data.order_by);
	let search_params = $state({ ...data.search_params });
	let default_params = $state(data.search_params);
	let pagination = $state();

	const update = (rat, rev, hp, cr, tp) => {
		comments = rat;
		ratings = rev;
		has_purchased = hp;
		can_comment = cr;
		total_page = tp;
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
	title="Review"
	description="Read honest reviews and ratings from verified customers to help you make confident buying decisions."
/>
<Log action={'viewed item review'} entity_key={item.key} entity_type={'item'} />

<Content --content-height="auto" --content-padding-bottom="0">
	<div class="line">
		<BackButton href="/{item.slug}" />
		<div class="page_title">
			Rating{comments.length ? 's' : ''} and review{comments.length ? 's' : ''}
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
			--select-height="32px"
			--select-padding-x="8px"
			--select-font-size="0.8rem"
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

		{#if !app.login}
			<Button icon="log-in" onclick={() => module.open(Login)}>Login to add review</Button>
		{:else if !has_purchased}
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
		{:else if can_comment}
			<Button
				icon="message-circle-plus"
				onclick={() => module.open(Add, { item, search_params, update })}
			>
				Add review
			</Button>
		{/if}
	</div>
</Content>

<Content>
	{#each comments as comment (comment.key)}
		<div class="comment" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
			<One {item} {comment} {search_params} {update}></One>
		</div>
	{:else}
		<PageNote>
			<Icon icon="message-circle-off" size="50" />
			No review
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

<style>
	.line {
		align-items: flex-end;
	}

	.comment {
		margin-top: 8px;

		&:first-child {
			margin-top: 0;
		}
	}
</style>
