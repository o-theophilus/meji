<script>
	import { Login } from '$lib/auth';
	import { Button, LinkArrow } from '$lib/button';
	import { Dialogue, PageNote } from '$lib/info';
	import { Card } from '$lib/layout';
	import { Icon, Spinner } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import Add from './_add.svelte';
	import One from './one.svelte';

	let { item, review, loading } = $props();

	let ratings = $derived(review.ratings);
	let reviews = $derived(review.reviews);
	let has_purchased = $derived(review.has_purchased);
	let can_review = $derived(review.can_review);

	let count = $derived.by(() => {
		let _temp = 0;
		if (ratings) {
			for (const x of ratings) {
				_temp += x.count;
			}
		}
		return _temp;
	});
	let open = $derived(count > 1);

	const update = (rat, rev, hp, cr, tp) => {
		reviews = rat;
		ratings = rev;
		has_purchased = hp;
		can_review = cr;
		open = true;
	};
</script>

<Card
	{open}
	onclick={() => (open = !open)}
	--card-title-padding="0"
	--card-content-padding="16px 0 0 0"
>
	{#snippet title()}
		<div class="title line">
			{#if count > 0}
				{count}
			{/if}
			Rating{#if count > 1}s{/if} & review{#if count > 1}s{/if}
			<Spinner active={loading} size="20" />
			<div class="hr"></div>
		</div>
	{/snippet}

	{#if open && !loading}
		{#each reviews as review (review.key)}
			<div class="item" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<One {item} {review} search={{ page_size: 3 }} {update}></One>
			</div>
		{:else}
			<PageNote>
				<Icon icon="message-circle-off" size="50" />
				No review
			</PageNote>
		{/each}

		<div class="bottom">
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
			{:else if can_review}
				<Button
					icon="message-circle-plus"
					onclick={() => module.open(Add, { item, search: { page_size: 3 }, update })}
				>
					Add review
				</Button>
			{/if}

			{#if count > 3}
				<LinkArrow href="/{item.slug}/review" --link-font-size="0.8rem">See All</LinkArrow>
			{/if}
		</div>
	{/if}
</Card>

<style>
	.title {
		display: flex;
		gap: 16px;
		font-weight: 800;
		color: var(--ft1);

		& .hr {
			background-color: var(--ft1);
			height: 2px;
			flex-grow: 1;
		}
	}

	.item {
		margin-top: 8px;
	}
	.item:first-child {
		margin-top: 0;
	}

	.bottom {
		margin-top: 16px;
		display: flex;
		justify-content: space-between;
		gap: 160x;
	}
</style>
