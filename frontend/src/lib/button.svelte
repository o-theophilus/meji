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
	<button class={clas} on:click|stopPropagation title={tooltip} {disabled}>
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
		fill: currentColor;
		
		text-decoration: none;
		font-weight: 500;

		width: fit-content;
		cursor: pointer;
	}

	:hover {
		background-color: var(--cl2);
		color: var(--ac5_);
	}
	.primary {
		background-color: var(--cl1);
		color: var(--ac5_);
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

	.round {
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

	.small {
		--size: 28px;
		gap: var(--sp1);
		padding: var(--sp1);
		font-size: smaller;
	}
	.wide {
		width: 100%;
		max-width: 400px;
	}

	button:disabled {
		opacity: 0.5;
		background-color: var(--ac4);
		cursor: unset;
		color: var(--ac2);
	}
</style>
