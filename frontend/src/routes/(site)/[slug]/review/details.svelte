<script>
	import { page } from '$app/state';
	import { Datetime, User } from '$lib/macro';
	import { scroll } from '$lib/store.svelte.js';
	import { onMount } from 'svelte';
	import Rating from './rating.svelte';
	let { comment, is_admin = false } = $props();

	onMount(() => {
		if (page.url.hash == `#${comment.key}`) {
			scroll(`#${comment.key}`);
		}
	});
</script>

<div class="user_date">
	<User user={comment.user}>
		{#if !is_admin}
			<div class="rating">
				<Rating value={comment.rating}></Rating>
			</div>
		{/if}
	</User>

	<div class="date"><Datetime datetime={comment.date_created} type="ago" /></div>
</div>

<div class="comment">
	{comment.comment}

	{#if !is_admin && comment.stats?.others_like}
		<div class="note">
			{comment.stats.others_like.toLocaleString()}
			{comment.stats.others_like > 1 ? 'people' : 'person'} found this helpful
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
