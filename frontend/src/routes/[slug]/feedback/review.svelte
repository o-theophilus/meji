<script>
	import { createEventDispatcher } from 'svelte';
	import Rating from '$lib/item/rating.svelte';
	import { user } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();
	export let feedback = {};
</script>

<section>
	<div class="details">
		<div class="left">
			<div class="img">
				<img
					src={feedback.user.photo ? feedback.user.photo : '/image/user.png'}
					alt={feedback.name}
				/>
			</div>
			<div class="info">
				<div class="name">
					{feedback.user.name}
				</div>
				<div class="date">
					{feedback.date}
				</div>
			</div>
		</div>
		<div class="rating">
			<Rating rating={feedback.rating} />
		</div>
	</div>
	<div class="comment">
		{feedback.review}
		<br />
		{#if $user.key == feedback.user.key}
			<Button
				class="small"
				on:click={() => {
					emit('edit');
				}}
				tooltip="Edit Feedback"
			>
				<SVG type="edit" size="12" />
			</Button>
		{/if}
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		gap: var(--sp2);
	}
	section:not(:last-child) {
		padding-bottom: var(--sp2);
		border-bottom: 2px solid var(--ac5);
	}

	.details,
	.left {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp2);
	}
	.info {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}

	.img {
		--size: 40px;

		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		overflow: hidden;
	}

	img {
		width: 100%;
		height: 100%;

		object-fit: cover;
	}

	.name {
		font-weight: 500;
	}

	.date {
		font-size: x-small;
		color: var(--ac3);
	}
</style>
