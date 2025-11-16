<script>
	import { page } from '$app/state';
	import { Icon } from '$lib/macro';
	let { name, icon, icon2, href = '', onclick } = $props();
	let active = $derived(href.split('/')[1] == page.url.pathname.split('/')[1]);
</script>

{#if href}
	<a class:active {href} data-sveltekit-preload-data>
		<Icon icon={!active ? icon : `${icon}_active`} size="24" />
		{name}
	</a>
{:else}
	<button onclick={() => onclick?.()}>
		<Icon icon={!active ? icon : `${icon}_active`} size="24" />
		{name}
	</button>
{/if}

<style>
	button {
		all: unset;
		cursor: pointer;
	}

	a,
	button {
		position: relative;

		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;

		padding: 16px;
		width: 100%;
		border-radius: 8px;

		color: var(--ft2);
		fill: var(--ft2);
		font-size: 0.8rem;
		text-decoration: none;
		line-height: 100%;

		transition:
			border-color var(--trans),
			color var(--trans),
			fill var(--trans),
			font-weight var(--trans),
			background-color var(--trans);
	}

	a:hover,
	button:hover {
		background-color: var(--bg2);
	}

	.active {
		font-weight: 600;
		color: var(--ft1);
		fill: var(--ft1);
		background-color: var(--bg2);
	}
</style>
