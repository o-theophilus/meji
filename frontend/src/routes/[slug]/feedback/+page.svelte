<script>
	import { module, portal, user } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Review from './review.svelte';
	import Rating from './rating.svelte';
	import Add from './_add.svelte';

	export let data;
	let { item } = data;
	$: feedbacks = data.feedbacks;

	$: if ($portal) {
		feedbacks.push($portal);
		$portal = '';
	}

	let give_feedback = true;
</script>

<section>
	{#if feedbacks.length > 0}
		<Card>
			<b>Rating</b>
			<br />
			<br />
			<Rating {feedbacks} />
		</Card>
	{/if}
	<Card>
		<b>Review{feedbacks.length > 1 ? 's' : ''}</b>
		<br />
		<br />
		{#each feedbacks as feedback (feedback.key)}
			<Review
				bind:feedback
				on:edit={() => {
					$module = {
						module: Add,
						item,
						feedback
					};
				}}
			/>
		{:else}
			{item.name} has no feedback yet.
			<br />
			Only
			{#if !$user.login}
				logged in
			{/if}
			customers who have purchased this item may leave a review.
		{/each}

		{#if give_feedback}
			<br />
			<br />
			<Button
				name="Give Feedback"
				on:click={() => {
					$module = {
						module: Add,
						item
					};
				}}
			/>
		{/if}
	</Card>
</section>

<!-- <Pagination /> -->
<style>
	section {
		display: flex;
		gap: var(--sp1);
		flex-direction: column;
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
	}
</style>
