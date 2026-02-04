<script>
	import { Icon } from '$lib/macro';

	let { active = '', like = 0, dislike = 0, onlike, ondislike } = $props();
</script>

<div class="group">
	<button class="like" onclick={onlike} class:active={active == 'like'}>
		<Icon icon="thumbs-up" />
		{#if like}
			{like}
		{/if}
	</button>

	<button class="dislike" onclick={ondislike} class:active={active == 'dislike'}>
		<Icon icon="thumbs-down" />
		{#if dislike}
			{dislike}
		{/if}
	</button>
</div>

<style>
	.group {
		display: flex;
		align-items: center;
		gap: 1px;
	}

	button {
		display: flex;
		align-items: center;
		gap: 4px;

		height: var(--like-height, 48px);
		padding: 4px 16px;
		font-size: 0.7rem;

		color: var(--like-color, var(--ft2));
		background-color: var(--like-background-color, var(--bg2));
		outline: 1px solid var(--like-outline-color, transparent);
		outline-offset: -1px;
		border: none;
		cursor: pointer;

		transition:
			background-color 0.2s ease-in-out,
			outline-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}
	.like {
		border-radius: var(--like-height, 48px) 0 0 var(--like-height, 48px);
	}
	.dislike {
		border-radius: 0 var(--like-height, 48px) var(--like-height, 48px) 0;
	}

	.active,
	button:hover {
		background-color: var(--like-background-color-hover, var(--cl1));
		outline-color: var(--like-outline-color-hover, transparent);
		color: white;
	}
</style>
