<script>
	import { page } from '$app/state';
	import { Icon } from '$lib/macro';
	import { quadIn } from 'svelte/easing';
	import { scale } from 'svelte/transition';
	let { name, icon, icon2, href = '', count, onclick } = $props();
	let active = $derived(href.split('/')[1] == page.url.pathname.split('/')[1]);
</script>

<a class:active {href} data-sveltekit-preload-data>
	<div class="block">
		<Icon icon={!active ? icon : `${icon}_active`} size="24" />
		{name}

		{#if count > 0}
			{#key count}
				<div class="count" in:scale={{ easing: quadIn }}>
					{count}
				</div>
			{/key}
		{/if}
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		justify-content: center;

		width: 100%;
		height: 100%;
		border-radius: 8px;

		text-decoration: none;

		transition: background-color var(--trans);
	}

	a:hover,
	.active {
		background-color: var(--bg2);
	}

	.block {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 4px;

		color: var(--ft2);
		fill: var(--ft2);
		font-size: 0.8rem;
		line-height: 100%;

		transition:
			color var(--trans),
			fill var(--trans),
			font-weight var(--trans);
	}

	.active .block {
		color: var(--ft1);
		fill: var(--ft1);
		font-weight: 600;
	}

	.count {
		position: absolute;
		top: 2px;
		right: 0;

		display: flex;
		align-items: center;
		justify-content: center;

		width: 12px;
		height: 12px;
		border-radius: 50%;

		font-size: 0.5rem;
		background-color: var(--cl1);
		color: white;
	}
</style>
