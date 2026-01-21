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
	import One from './one.svelte';
	import Add from './_add.svelte';
	import Control from './one.control.svelte';

	let { item } = $props();
	let reviews = $state([]);

	let order_by = $state([]);
	let open = $state(false);
	let loading = $state(true);
	let search = $state({
		order: 'most_like',
		page_no: 1,
		page_size: 3
	});

	const update = (data) => {
		reviews = data;
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

			order_by = resp.order_by;
			if (reviews.length) open = true;
		}

		loading = false;
	};
</script>

<Card
	{open}
	onclick={() => (open = !open)}
	--card-title-border-color="var(--bg2)"
	--card-title-padding="16px 0"
	--card-content-padding="0"
>
	{#snippet title()}
		<div class="line">
			<div class="title">
				{#if reviews.length > 0}
					{reviews.length}
				{/if}
				Review{#if reviews.length > 1}s{/if}
			</div>
			<Spinner active={loading} size="20" />
		</div>
		<LinkArrow href="/{item.slug}/review" --link-font-size="0.8rem">See All</LinkArrow>
	{/snippet}

	{#if open && !loading}
		<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<!-- {#if reviews.length > 1}
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
						load();
					}}
				/>
			{/if} -->

			{#each reviews as review (review.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<One {review}>
						{#snippet parent()}
							{#each reviews as x}
								{#if review.parent_key == x.key}
									<One review={x}></One>
								{/if}
							{/each}
						{/snippet}
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
		</div>
	{/if}
</Card>

<div class="button">
	{#if app.login}
		<Button icon="message-circle-plus" onclick={() => module.open(Add, { item, update, search })}>
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
</style>
