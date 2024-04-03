<script>
	export let hide = false;
	export let active = false;
	export let no_grow;
</script>

<button on:click class:hide class:active class:grow={!no_grow}>
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

	button:hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
	.hide {
		display: none;
	}
	.active {
		background-color: var(--cl1);
		color: var(--ac6_);
	}
</style>
