<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { user, state } from '$lib/store.js';

	import Link from '$lib/button/link.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
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

<div class="v_margin" class:open>
	<div class="row space" class:open>
		<div class="row">
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
		<div class="row">
			{#if feedbacks.length > 0}
				<Link href="/{item.slug}/feedback" on:click={click} on:mouseenter={click} icon>
					view more
				</Link>
			{/if}
			{#if give_feedback && feedbacks.length > 0} | {/if}
			{#if give_feedback}
				<Link href="/{item.slug}/feedback?add=true" on:click={click} on:mouseenter={click} icon>
					add review
				</Link>
			{/if}
		</div>

		<div transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			{#each feedbacks as feedback}
				<Review {feedback} {item} />
			{:else}
				<div class="v_margin">
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
					<br />
					<br />
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.space {
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}
	/* .open {
		margin-bottom: 0;
	} */

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 700;
	}
</style>
