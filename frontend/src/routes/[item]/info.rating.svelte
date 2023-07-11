<script>
	import Rating from '$lib/item/rating.svelte';

	export let item;

	let rating = 0;
	if (item.feedbacks) {
		for (let i in item.feedbacks) {
			rating += item.feedbacks[i].rating;
		}
		rating /= item.feedbacks.length;
	}
</script>

{#if item.feedbacks && item.feedbacks.length > 0}
	<div class="rating">
		<Rating {rating} />
		<div>
			{item.feedbacks.length} rating{#if item.feedbacks.length > 1}s{/if}
		</div>
	</div>
{/if}

<style>
	.rating {
		display: flex;
		align-items: center;

		gap: var(--sp1);

		color: var(--ac2);
	}
</style>
