<script>
	export let disabled = false;
	export let active = false;
	export let no_grow = false;
</script>

<button class:active class:grow={!no_grow} on:click {disabled}>
	<slot />
</button>

<style>
	button {
		--size: 24px;

		border: none;
		height: var(--size);
		border-radius: calc(var(--size) / 2);
		padding: 0 var(--sp2);

		font-size: small;
		cursor: pointer;
		background-color: var(--cl1_t);

		text-transform: capitalize;
		color: var(--ac1);
	}
	.grow {
		flex-grow: 1;
	}

	:disabled {
		background-color: var(--ac5);
		color: var(--ac2);
		cursor: unset;
		opacity: 0.4;
	}

	:not(:disabled).active {
		background-color: var(--cl1);
		color: var(--ac6_);
	}
	:not(:disabled):hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
</style>
