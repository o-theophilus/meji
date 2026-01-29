<script>
	import { onMount } from 'svelte';

	let { value = $bindable(), list = ['on', 'off'], onclick } = $props();
	if (!value || !list.includes(value)) {
		value = list[0];
	}
</script>

<div class="radio">
	{#each list as x}
		<button
			class:empty={x == ''}
			class:active={x == value}
			onclick={() => {
				if (value == x) return;
				value = x;
				onclick?.(value);
			}}
		>
			{x}
		</button>
	{/each}
	<div class="hover"></div>
</div>

<style>
	.radio {
		position: relative;
		z-index: 0;

		display: flex;

		width: min-content;
		height: var(--button-height, 48px);
		border-radius: var(--button-border-radius, 4px);
		background-color: var(--bg);

		border: 1px solid var(--button-border-color, var(--ol));
		padding: 2px;
		overflow: hidden;
		flex-shrink: 0;
		transition: border-color 0.2s ease-in-out;

		&:hover {
			border-color: var(--button-border-color-hover, var(--ft1));
		}
	}

	button {
		all: unset;

		padding: 0 var(--button-padding-x, 16px);
		background-color: transparent;
		border-radius: var(--button-border-radius, 4px);
		z-index: 1;
		min-width: var(--button-height);
		font-size: var(--button-font-size, 0.8rem);

		&:hover:not(.active) {
			background-color: var(--bg1);
		}
		&.active {
			color: white;
			font-weight: 800;
			anchor-name: --active;
		}

		&.empty {
			padding: 0;
		}

		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;
	}

	.hover {
		position-anchor: --active;
		position: absolute;
		top: anchor(top);
		bottom: anchor(bottom);
		right: anchor(right);
		left: anchor(left);

		background-color: var(--cl1);
		border-radius: var(--button-border-radius, 4px);

		transition:
			top 0.2s ease-in-out,
			bottom 0.2s ease-in-out,
			right 0.2s ease-in-out,
			left 0.2s ease-in-out;
	}
</style>
