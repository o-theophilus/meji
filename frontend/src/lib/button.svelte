<script>
	export let href = '';
	export let tooltip = '';
	export let target = '';
	export let disabled = false;
	let clas = '';
	export { clas as class };
</script>

{#if href}
	<a class={clas} {href} {target} title={tooltip}>
		<slot />
	</a>
{:else}
	<button class={clas} on:click title={tooltip} {disabled}>
		<slot />
	</button>
{/if}

<style>
	button,
	a {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);

		padding: var(--sp1) var(--sp2);
		border: none;
		border-radius: var(--sp0);
		width: fit-content;

		background-color: var(--ac5);
		color: var(--ac2);
		fill: currentColor;
		text-decoration: none;
		text-align: center;
		font-weight: 700;
		cursor: pointer;
	}

	.primary {
		background-color: var(--cl1);
		color: var(--ac6_);
		box-shadow: 0 -4px 0 var(--cl1_b) inset;
	}

	.large {
		padding: var(--sp2) var(--sp4);
		font-size: large;
	}
	.small {
		padding: var(--sp0);
		gap: var(--sp0);
		font-size: small;
		min-width: 28px;
	}
	.wide {
		width: 100%;
	}

	.round {
		--size: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;

		width: var(--size);
		height: var(--size);

		padding: 0;

		border-radius: var(--size);
	}

	.round.large {
		--size: 40px;
	}

	:hover:not(:disabled) {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
	.hover_red:hover:not(:disabled) {
		background-color: var(--cl4);
	}

	:disabled {
		background-color: var(--ac5);
		color: var(--ac2);
		box-shadow: unset;

		cursor: unset;
		opacity: 0.4;
	}

	.link {
		display: inline-flex;
		gap: var(--sp0);
		padding: 0;
		color: var(--cl1);
		background: none;

		text-align: left;
	}
	.link:hover {
		color: var(--cl1_b);
	}

	.outline {
		outline: 2px solid var(--ac4);
	}
	.outline:hover {
		outline-color: var(--ac5);
	}
</style>
