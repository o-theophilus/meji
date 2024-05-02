<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, state } from '$lib/store.js';

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

	let loading_feedbacks = true;

	export const get_feedback = async () => {
		loading_feedbacks = true;
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/feedback/${item.key}/${$user.key}?size=5`
		);
		resp = await resp.json();
		loading_feedbacks = false;

		if (resp.status == 200) {
			feedbacks = resp.feedbacks;
			give_feedback = resp.give_feedback;
			// open = feedbacks.length > 0;
		}
	};

	const click = () => {
		let sn = 'item';
		let i = $state.findIndex((x) => x.name == sn);
		if (i == -1) {
			$state.push({
				name: sn,
				data: item
			});
		} else {
			$state[i].data = item;
		}
	};
</script>

<div class="horizontal">
	<div class="horizontal">
		<span class="bold">
			Customer{feedbacks.length > 1 ? 's' : ''} Feedback
		</span>
		<Spinner active={loading_feedbacks} size="16" />
		<Rating ratings={item.ratings} />
	</div>

	{#if !loading_feedbacks}
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
	{/if}
</div>

{#if open}
	<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#each feedbacks as feedback}
			<Review {feedback} {item} />
		{:else}
			<span>
				There is no feedback yet.
				<br />
				{#if give_feedback}
					Be the first to add a review.
				{:else}
					Only
					{#if !$user.login}
						logged in
					{/if}

					customers who have purchased this item can add a review.
				{/if}
			</span>
			<br />
		{/each}

		{#if give_feedback || feedbacks.length > 0}
			<br />
		{/if}
		{#if give_feedback}
			<Button
				class="link"
				href="/{item.slug}/feedback?add=true"
				on:click={click}
				on:mouseenter={click}>Add Review</Button
			>
		{/if}
		{#if give_feedback && feedbacks.length > 0}
			&nbsp; &nbsp;
		{/if}
		{#if feedbacks.length > 0}
			<Button href="/{item.slug}/feedback" class="link" on:click={click} on:mouseenter={click}>
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
