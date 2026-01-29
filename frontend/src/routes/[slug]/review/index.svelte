<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Button, FoldButton, LinkArrow } from '$lib/button';
	import { Login } from '$lib/auth';
	import { Icon, Spinner } from '$lib/macro';
	import { Dropdown } from '$lib/input';
	import { PageNote } from '$lib/info';
	import { Card } from '$lib/layout';
	import Add from './_add.svelte';
	import One from './one.svelte';

	let { item } = $props();
	let reviews = $state([]);

	let ratings = $state([]);

	let order_by = $state([]);
	let open = $state(false);
	let loading = $state(true);
	let count = $derived.by(() => {
		let _temp = 0;
		for (const x of ratings) {
			_temp += x.count;
		}
		return _temp;
	});
	let search = $state({
		order: 'most relevant ▼',
		page_no: 1,
		page_size: 3
	});

	const update = (a, b, c) => {
		reviews = a;
		ratings = b;
		open = true;
	};

	export const load = async () => {
		loading = true;

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/review/${item.key}?${new URLSearchParams(search).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			reviews = resp.reviews;
			ratings = resp.ratings;
			order_by = resp.order_by;
			if (reviews.length) open = true;
		}

		loading = false;
	};
</script>

<Card
	{open}
	onclick={() => (open = !open)}
	--card-title-border-color="var(--bg1)"
	--card-title-padding="16px 0"
	--card-content-padding="0"
>
	{#snippet title()}
		<div class="line">
			<div class="title">
				{#if reviews.length > 0}
					{count}
				{/if}
				Rating{#if reviews.length > 1}s{/if} and review{#if reviews.length > 1}s{/if}
			</div>
			<Spinner active={loading} size="20" />
		</div>
		{#if count > 3}
			<LinkArrow href="/{item.slug}/review" --link-font-size="0.8rem">See All</LinkArrow>
		{/if}
	{/snippet}

	{#if open && !loading}
		<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each reviews as review (review.key)}
				<div class="item" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<One {item} {review} {search} {update}></One>
				</div>
			{:else}
				<PageNote>
					<Icon icon="message-circle-off" size="50" />
					No review
				</PageNote>
			{/each}
		</div>
	{/if}
</Card>

<div class="button">
	{#if app.login}
		<Button icon="message-circle-plus" onclick={() => module.open(Add, { item, search, update })}>
			Add review
		</Button>
	{:else}
		<Button icon="log-in" onclick={() => module.open(Login)}>Login to add review</Button>
	{/if}
</div>

<style>
	.title {
		font-weight: 800;
	}

	.button {
		margin: 16px 0;
	}

	.item {
		margin-top: 8px;
	}
	.item:first-child {
		margin-top: 0;
	}
</style>
