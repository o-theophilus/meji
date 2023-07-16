<script>
	import SVG from '$lib/comp/svg.svelte';

	export let href = '';

	export let name = '';
	export let tooltip = '';
	export let icon = '';
	export let icon_size = 20;
	export let color = '';
	export let active = false;
	let clas = '';
	export { clas as class };
	export let target = '';

	// let icon_only = !(name || $$slots);
	let icon_only = !name;
</script>

{#if href}
	<a
		class={clas}
		class:active
		class:icon_only
		style:color
		style:fill={color}
		{href}
		{target}
		title={tooltip}
	>
		<SVG type={icon} size={icon_size} />
		{name}
		<slot />
	</a>
{:else}
	<button
		class={clas}
		class:active
		class:icon_only
		style:color
		style:fill={color}
		on:click|stopPropagation
		title={tooltip}
	>
		<SVG type={icon} size={icon_size} />
		{name}
		<slot />
	</button>
{/if}

<style>
	button,
	a {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp2);

		border: none;
		padding: var(--sp2);
		border-radius: var(--sp0);

		background-color: var(--ac4);
		color: var(--ac2);
		fill: var(--ac2);

		text-decoration: none;
		font-weight: 500;

		width: fit-content;
		cursor: pointer;
	}

	.active,
	.primary {
		background-color: var(--cl1);
		color: var(--ac5_);
		fill: var(--ac5_);
	}
	.secondary {
		background-color: transparent;
		color: var(--ac3);
		border: 2px solid var(--ac5);
	}

	.tertiary {
		padding: 0;
		border-radius: 0;
		color: var(--ac1);

		background-color: transparent;
		border-bottom: 2px solid var(--ac5);
	}
	.link {
		display: inline;
		padding: 0;
		color: var(--cl1);
		background-color: transparent;
	}

	.tiny {
		gap: var(--sp1);
		padding: var(--sp1);
		font-size: small;
	}
	.tag {
		--size: 24px;
		height: var(--size);
		padding: 8px;

		border-radius: calc(var(--size) / 2);

		font-size: x-small;
		font-weight: unset;
	}
	.wide {
		width: 100%;
	}
	.wide2 {
		width: 100%;
		max-width: 400px;
	}

	.icon_only {
		--size: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		padding: 0;

		border-radius: var(--size);
	}

	.icon_only.tiny {
		--size: 20px;

		width: var(--size);
		height: var(--size);
	}

	:hover {
		background-color: var(--cl1);
		color: var(--ac5_);
		fill: var(--ac5_);
	}

	.active:hover,
	.primary:hover {
		background-color: var(--cl2);
	}
	.tertiary:hover {
		background-color: transparent;
		border-color: var(--cl1);
		color: var(--cl1);
	}
	.secondary:hover {
		background-color: transparent;
		color: var(--cl1);
		border: 2px solid var(--cl1);
	}

	.hover_red:hover {
		background-color: var(--cl4);
	}
	.link:hover {
		background-color: transparent;
		color: var(--cl2);
	}
</style>
