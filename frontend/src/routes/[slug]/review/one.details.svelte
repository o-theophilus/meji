<script>
	import { Datetime, Avatar } from '$lib/macro';
	import Rating from './rating.svelte';
	let { review, admin = false } = $props();
</script>

<section>
	<div class="avatar_name_date">
		<Avatar name={review.user.name} photo={review.user.photo} --avatar-border-radius="50%" />

		<div class="name_date">
			<div class="name_username">
				<div class="name">{review.user.name}</div>
				<div class="username">
					@{review.user.username}
					{#if admin}
						(Admin)
					{/if}
				</div>
			</div>

			<div class="date"><Datetime datetime={review.date_created} type="ago" /></div>
		</div>
	</div>

	<div class="comment">
		{#if !admin}
			<div class="rating">
				<Rating value={review.rating}></Rating>
			</div>
		{/if}
		{review.comment}
	</div>
</section>

<style>
	.avatar_name_date {
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.name_date {
		display: flex;
		align-items: flex-start;
		gap: 8px 16px;
		justify-content: space-between;
		flex-wrap: wrap;

		width: 100%;
	}

	.name {
		color: var(--ft1);
		font-size: 0.8rem;
		font-weight: 800;
		line-height: 100%;
		margin-bottom: 4px;
	}

	.date {
		font-size: 0.8rem;
		line-height: 100%;
	}

	.username {
		font-size: 0.8rem;
	}

	.rating {
		margin-bottom: 8px;
	}
	.comment {
		margin-top: 16px;
		font-size: 0.9rem;
	}
</style>
