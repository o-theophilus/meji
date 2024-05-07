<script>
	import { user, module } from '$lib/store.js';

	import Rating from '$lib/item/rating.svelte';
	import Add from './_add.svelte';

	import Datetime from '$lib/datetime.svelte';
	import Link from '$lib/button/link.svelte';
	import SVG from '$lib/svg.svelte';

	export let feedback;
	export let item;
	export let editable = false;
</script>

<section>
	<img
		src={feedback.user_photo ? `${feedback.user_photo}/100` : '/image/user.png'}
		alt={feedback.name}
	/>
	<div class="right">
		<div class="row">
			<span class="name">
				{feedback.user_name}
			</span>
			<Rating rating={feedback.rating} />
		</div>
		<span class="date">
			<Datetime datetime={feedback.date} type="date" />
			<Datetime datetime={feedback.date} type="time" />
		</span>

		<div class="fbk">
			{feedback.review}
		</div>

		{#if $user.key == feedback.user_key && editable}
			<br />
			<Link
				on:click={() => {
					$module = {
						module: Add,
						item,
						feedback
					};
				}}
			>
				<SVG icon="edit" size="10" />
				Edit
			</Link>
		{/if}
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp2);
		margin: var(--sp2) 0;
		padding-top: var(--sp2);
		border-top: 2px solid var(--ac4);
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

	.row {
		display: flex;
		align-items: flex-start;
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

	.fbk {
		margin-top: var(--sp1);
	}
</style>
