<script>
	import { createEventDispatcher } from 'svelte';
	import Rating from './rating_star.svelte';
	import { user } from '$lib/store.js';

	let emit = createEventDispatcher();
	export let feedback = {};
</script>

<section>
	<div class="details">
		<div class="left">
			<div class="img">
				<img src={feedback.photo ? feedback.photo : '/image/user.png'} alt={feedback.name} />
			</div>
			<div class="info">
				<div class="name">
					{feedback.name}
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
		{#if $user?.key == feedback.user_key}
			<div
				on:click={() => {
					emit('ok');
				}}
			>
				edit
			</div>
		{/if}
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		gap: var(--gap2);
	}
	section:not(:last-child) {
		padding-bottom: var(--gap2);
		border-bottom: 2px solid var(--background);
	}

	.details,
	.left {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--gap2);
	}
	.info {
		display: flex;
		flex-direction: column;
		gap: var(--gap1);
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
		color: var(--midtone);
	}
</style>
