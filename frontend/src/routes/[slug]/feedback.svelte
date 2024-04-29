<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import SVG from '$lib/svg.svelte';
	import Rating from '$lib/item/rating.svelte';
	import Review from './feedback/review.svelte';
	import Spinner from '$lib/loading_spinner.svelte';

	export let item = {};
	let feedbacks = [];
	let give_feedback = false;
	let open = false;

	let emit = createEventDispatcher();

	let loading_feedbacks = true;
	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/feedback/${item.key}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		resp = await resp.json();
		loading_feedbacks = false;
		emit('done');

		if (resp.status == 200) {
			feedbacks = resp.feedbacks;
			give_feedback = resp.give_feedback;
			open = feedbacks.length > 0;
		}
	});
</script>

<div class="horizontal">
	<div class="horizontal">
		<span class="bold">
			Customer{feedbacks.length > 1 ? 's' : ''} Feedback
		</span>
		<Spinner active={loading_feedbacks} size="16" />
		<Rating ratings={item.ratings} />
	</div>

	<ButtonFold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</div>

{#if open}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#each feedbacks as feedback}
			<Review {feedback} {item} />
		{:else}
			<span>
				There is no feedback yet.
				<br />
				Only
				{#if !$user.login}
					logged in
				{/if}

				customers who have purchased this item can add a review.
			</span>
			<br />
		{/each}

		{#if give_feedback || feedbacks.length > 0}
			<br />
		{/if}
		{#if give_feedback}
			<Button class="link" href="/{item.slug}/feedback?add=true">Add Review</Button>
		{/if}
		{#if give_feedback && feedbacks.length > 0}
			&nbsp; &nbsp;
		{/if}
		{#if feedbacks.length > 0}
			<Button href="/{item.slug}/feedback" class="link">
				View all
				<SVG type="arrow_right" size="16" />
			</Button>
		{/if}
	</div>
	<br />
{/if}

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 700;
	}
</style>
