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
</div>

<style>
	.radio {
		position: relative;
		z-index: 0;

		display: flex;

		width: min-content;
		border-radius: var(--toggle-border-radius, 4px);
		background-color: var(--bg);

		border: 1px solid var(--toggle-border-color, var(--ol));
		padding: 2px;
		overflow: hidden;
		flex-shrink: 0;
		transition: border-color 0.2s ease-in-out;

		&:hover {
			border-color: var(--toggle-border-color-hover, var(--ft1));
		}
	}

	button {
		all: unset;
		cursor: pointer;

		height: var(--toggle-height, 42px);
		padding: 0 var(--toggle-padding-x, 16px);
		border-radius: var(--toggle-border-radius, 4px);
		width: max-content;

		background-color: transparent;
		font-size: var(--toggle-font-size, 1rem);

		&:hover:not(.active) {
			background-color: var(--bg1);
		}
		&.active {
			color: white;
			anchor-name: --active;
		}

		&.empty {
			padding: 0;
			aspect-ratio: 1;
		}

		transition:
			background-color 0.2s ease-in-out,
			color 0.2s ease-in-out;

		&::before {
			content: '';
			position-anchor: --active;
			z-index: -1;

			position: absolute;
			top: anchor(top);
			bottom: anchor(bottom);
			right: anchor(right);
			left: anchor(left);

			background-color: var(--cl1);
			border-radius: var(--toggle-border-radius, 4px);

			transition:
				top 0.2s ease-in-out,
				bottom 0.2s ease-in-out,
				right 0.2s ease-in-out,
				left 0.2s ease-in-out;
		}
	}
</style>
