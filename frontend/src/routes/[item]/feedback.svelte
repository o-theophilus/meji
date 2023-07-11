<script>
	import { goto } from '$app/navigation';

	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_fold.svelte';

	import Review from '$lib/comp/feedback_review.svelte';
	import Rating from '$lib/comp/rating.svelte';

	import HR from '$lib/comp/hr.svelte';
	import Button from '$lib/button.svelte';
	import Button_Fold from '$lib/comp/button_fold.svelte';

	export let item;
	let review_lenght = 3;
	let open = item.feedbacks && item.feedbacks.length > 0;
	let s = item.feedbacks && item.feedbacks.length > 1 ? 's' : '';
</script>

<Title title="Customer{s} Feedback">
	<Button_Fold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</Title>
{#if open}
	<Body>
		<section>
			{#if item.feedbacks && item.feedbacks.length > 0}
				<span class="title"> Rating </span>
				<Rating feedback={item.feedbacks} />
				<span class="title"> Reviews </span>

				{#each item.feedbacks.slice(0, review_lenght) as feedback (feedback.id)}
					<Review {feedback} />
				{/each}

				{#if item.feedbacks.length > review_lenght}
					<HR />
					<Button
						name="View all ({item.feedbacks.length})"
						class="tertiary"
						on:click={() => {
							goto(`/${item.id}/feedback`);
						}}
					/>
				{/if}
			{:else}
				There is no feedback yet.
				<br />
				<br />
				Only logged in customers who have purchased this item may leave a review.
			{/if}
		</section>
	</Body>
{/if}

<style>
	section {
		display: grid;
		gap: var(--sp2);
	}
	.title {
		font-weight: 500;
	}
</style>
