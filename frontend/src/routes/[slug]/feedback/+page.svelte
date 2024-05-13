<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module, portal, user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';
	import Button from '$lib/button/button.svelte';
	import Back from '$lib/button/back.svelte';
	import Center from '$lib/center.svelte';
	import Pagination from '$lib/pagination.svelte';
	import OrderBy from '$lib/order_by.svelte';
	import Meta from '$lib/meta.svelte';
	import UpdateUrl from '$lib/update_url.svelte';

	import Review from './review.svelte';
	import Rating from './rating.svelte';
	import Add from './_add.svelte';

	export let data;
	$: item = data.item;
	$: feedbacks = data.feedbacks;
	$: ratings = data.ratings;
	$: give_feedback = data.give_feedback;
	$: total_page = data.total_page;
	let { order_by } = data;

	$: if ($portal && $portal.type == 'feedback') {
		feedbacks = $portal.data.feedbacks;
		give_feedback = $portal.data.give_feedback;
		$portal = '';
	}

	const add = () => {
		$module = {
			module: Add,
			item
		};
	};

	onMount(() => {
		if ($page.url.searchParams.has('add')) {
			$page.url.searchParams.delete('add');
			window.history.replaceState(history.state, '', $page.url.href);
			if (give_feedback) {
				add();
			}
		}
	});
</script>

<UpdateUrl />
<Meta title={item.name} description={item.info} image="{item.photos[0]}/200" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Feedback{feedbacks.length > 1 ? 's' : ''}

		<svelte:fragment slot="right">
			<OrderBy {order_by} />
		</svelte:fragment>
	</Title>
</Center>

<Card>
	<section>
		{#if feedbacks.length > 0}
			<div>
				<Title card>
					<span class="bold">Rating</span>
				</Title>
				<Rating {ratings} />
			</div>
		{/if}

		<div>
			<Title card>
				<span class="bold">Review{feedbacks.length > 1 ? 's' : ''}</span>
			</Title>
			{#each feedbacks as feedback (feedback.key)}
				<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
					<Review editable {feedback} {item} />
				</div>
			{:else}
				{item.name} has no feedback yet.
				<br />
				Only
				{#if !$user.login}
					logged in
				{/if}
				customers who have purchased this item can add a review.
			{/each}

			{#if give_feedback}
				<br />
				<br />
				<Button on:click={add}>Add Review</Button>
			{/if}
		</div>
	</section>

	<Pagination {total_page} />
</Card>

<style>
	section {
		display: flex;
		gap: var(--sp4);
		flex-direction: column;
	}
	section > * {
		width: 100%;
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: row-reverse;
		}
	}

	.bold {
		color: var(--ac1);
	}
</style>
