<script>
	import { page } from '$app/state';
	import { scroll } from '$lib/store.svelte.js';
	import { Datetime, Avatar } from '$lib/macro';
	import { onMount } from 'svelte';
	import Rating from './rating.svelte';
	let { review, is_admin = false } = $props();

	onMount(() => {
		if (page.url.hash == `#${review.key}`) {
			scroll(`#${review.key}`);
		}
	});
</script>

<section>
	<div class="avatar_name_date">
		<Avatar name={review.user.name} photo={review.user.photo} --avatar-border-radius="50%" />

		<div class="name_date">
			<div class="name_username">
				<div class="name">{review.user.name}</div>
				<div class="username">
					@{review.user.username}
					{#if is_admin}
						(Admin)
					{/if}
				</div>
			</div>

			<div class="date"><Datetime datetime={review.date_created} type="ago" /></div>
		</div>
	</div>

	<div class="comment">
		{#if !is_admin}
			<div class="rating">
				<Rating value={review.rating}></Rating>
			</div>
		{/if}

		{review.comment}

		{#if !is_admin && review.stats?.others_like}
			<div class="note">
				{review.stats.others_like.toLocaleString()}
				{review.stats.others_like > 1 ? 'people' : 'person'} found this helpful
			</div>
		{/if}
	</div>
</section>

<style>
	section {
		padding: 16px;
	}

	.avatar_name_date {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.name_date {
		display: flex;
		gap: 4px 16px;
		justify-content: space-between;
		flex-wrap: wrap;
		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-weight: 600;
		line-height: 100%;
	}

	.date {
		line-height: 100%;
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
	}

	.username,
	.name,
	.note,
	.date {
		font-size: 0.8rem;
	}
</style>
