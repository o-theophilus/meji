<script>
	export let href = '';
	export let target = '';
	export let tooltip = '';
	export let disabled = false;

	export let size = ''; // large
	export let extra = ''; // outline:not(primary), hov_red:not(primary)
</script>

<!-- TODO: remove a element -->
{#if href}
	<a
		{href}
		class:large={size == 'large'}
		class:outline={extra == 'outline'}
		class:hover_red={extra == 'hover_red'}
		{target}
		title={tooltip}
	>
		<slot />
	</a>
{:else}
	<button
		on:click
		class:large={size == 'large'}
		class:outline={extra == 'outline'}
		class:hover_red={extra == 'hover_red'}
		title={tooltip}
		{disabled}
	>
		<slot />
	</button>
{/if}

<style>
	button,
	a {
		--size: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		border: none;
		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		background-color: var(--ac5);
		fill: var(--ac2);
		cursor: pointer;
	}

	.large {
		--size: 40px;
	}

	:disabled {
		background-color: var(--ac5);
		color: var(--ac2);
		box-shadow: unset;

		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled):hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
	:not(:disabled).hover_red:hover {
		background-color: var(--cl4);
	}

	:not(:disabled).outline {
		outline: 2px solid var(--ac4);
	}
</style>
