<script>
	import { user, module } from '$lib/store.js';

	import Rating from '$lib/item/rating.svelte';
	import Add from './_add.svelte';

	import Datetime from '$lib/datetime.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	export let feedback;
	export let item;
	export let editable = false;
</script>

<section>
	<img src={feedback.user.photo ? feedback.user.photo : '/image/user.png'} alt={feedback.name} />
	<div class="right">
		<div class="up">
			<div>
				<span class="name">
					{feedback.user.name}
				</span>
				<br />
				<span class="date">
					<Datetime datetime={feedback.date} type="date" />
					<Datetime datetime={feedback.date} type="time" />
				</span>
			</div>
			<Rating rating={feedback.rating} />
		</div>
		<br />
		{feedback.review}
		{#if $user.key == feedback.user.key && editable}
			<Button
				class="link"
				on:click={() => {
					$module = {
						module: Add,
						item,
						feedback
					};
				}}
				tooltip="Edit Feedback"
			>
				<SVG type="edit" size="10" />
				Edit
			</Button>
		{/if}
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp2);
		padding: var(--sp2) 0;
		border-bottom: 1px solid var(--ac4);
	}

	img {
		--size: 40px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
	}

	.right {
		width: 100%;
	}

	.up {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--sp2);
	}
	.name {
		font-weight: 700;
		color: var(--ac1);
	}

	.date {
		font-size: smaller;
		color: var(--ac3);
	}
</style>
