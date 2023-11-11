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
		font-weight: 500;
		cursor: pointer;
	}

	:hover {
		background-color: var(--cl2);
		color: var(--ac6_);
	}
	.primary {
		background-color: var(--cl1);
		color: var(--ac6_);
		box-shadow: 0 -4px 0 var(--cl2) inset;
	}
	.primary:hover {
		background-color: var(--cl2);
	}
	.link {
		display: inline-flex;
		gap: var(--sp0);
		padding: 0;
		color: var(--cl1);
		background: none;
	}
	.link:hover {
		color: var(--cl2);
	}
	.hover_red:hover {
		background-color: var(--cl4);
	}

	.large {
		padding: var(--sp2) var(--sp4);
		font-size: large;
	}
	.small {
		font-size: small;
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

	.wide {
		width: 100%;
		/* max-width: 400px; */
	}

	.hover_red:disabled,
	button:disabled,
	.primary:disabled {
		background-color: var(--ac5);
		outline: 2px solid var(--ac5);
		color: var(--ac4);
		cursor: unset;
		box-shadow: unset;
	}

	.outline {
		outline: 2px solid var(--ac4);
	}
	.outline:hover {
		outline-color: var(--ac5);
	}
</style>
