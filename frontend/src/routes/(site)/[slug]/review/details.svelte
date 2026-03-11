<script>
	import { page } from '$app/state';
	import { Datetime, User } from '$lib/macro';
	import { scroll } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Rating from './rating.svelte';
	let { review, is_admin = false } = $props();

	onMount(() => {
		if (page.url.hash == `#${review.key}`) {
			scroll(`#${review.key}`);
		}
	});
</script>

<div class="user_date">
	<User user={review.user}>
		{#if !is_admin}
			<div class="rating">
				<Rating value={review.rating}></Rating>
			</div>
		{/if}
	</User>

	<div class="date"><Datetime datetime={review.date_created} type="ago" /></div>
</div>

<div class="comment">
	{review.comment}

	{#if !is_admin && review.stats?.others_like}
		<div class="note">
			{review.stats.others_like.toLocaleString()}
			{review.stats.others_like > 1 ? 'people' : 'person'} found this helpful
		</div>
	{/if}
</div>

<style>
	.user_date {
		display: flex;
		justify-content: space-between;
		gap: 16px;
	}

	.date {
		line-height: 100%;
		font-size: 0.7rem;
	}

	.rating {
		margin-bottom: 8px;
	}
	.comment {
		margin-top: 16px;
	}
	.note {
		margin-top: 16px;
		font-style: italic;
		font-size: 0.8rem;
	}
</style>
