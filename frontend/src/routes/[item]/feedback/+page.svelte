<script context="module">
	export async function load({ fetch, params, session }) {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}/feedback/${params.item}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: session.token
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				return {
					props: {
						item: resp.data.item,
						give_feedback: resp.data.give_feedback
					}
				};
			} else {
				return {
					status: 404,
					error: resp.message
				};
			}
		}
		return {
			status: 404,
			error: 'Oops! something went wrong'
		};
	}
</script>

<script>
	import { module, _tick } from '$lib/store.js';

	import Pagination from '$lib/comp/pagination.svelte';

	import Card from '$lib/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/button.svelte';

	import Review from '$lib/comp/feedback_review.svelte';
	import Rating from '$lib/comp/rating.svelte';

	import Add from '$lib/comp/feedback_form.svelte';

	export let item;
	export let give_feedback;

	$: if ($_tick) {
		item = $_tick;
		$_tick = '';
	}
</script>

<section>
	{#if item.feedbacks.length > 0}
		<Card>
			<Title title="Rating" />
			<Body>
				<Rating feedback={item.feedbacks} />
			</Body>
		</Card>
	{/if}
	<Card>
		<Title title="Reviews" />
		<Body>
			{#each item.feedbacks as feedback (feedback.key)}
				<Review
					{feedback}
					on:ok={() => {
						$module = {
							module: Add,
							data: {
								item,
								feedback
							}
						};
					}}
				/>
			{:else}
				<strong>{item.name}</strong> has no feedback yet.
				<br />
				Only logged in customers who have purchased this item may leave a review.
			{/each}

			{#if give_feedback}
				<Button
					name="Give Feedback"
					on:click={() => {
						$module = {
							module: Add,
							data: {
								item
							}
						};
					}}
				/>
			{/if}
		</Body>
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
