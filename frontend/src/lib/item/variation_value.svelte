<script>
	export let active = false;
	export let value;
	export let button = false;
	$: v = value.split(':');
</script>

<button class:active class:button on:click>
	{#if v[0]}
		<div class="name">{v[0]}</div>
	{/if}

	{#if v[1]}
		<div class="color" style:background-color={v[1]} />
	{/if}
</button>

<style>
	button {
		display: inline-flex;
		align-items: center;
		justify-content: center;

		--size: 32px;
		height: var(--size);

		border-radius: var(--size);
		border: 2px solid transparent;

		color: var(--ac2);
		background-color: var(--ac4);
	}
	.button {
		cursor: pointer;
	}

	.active {
		border-color: var(--cl1);
	}

	.name {
		padding: var(--sp1);
	}

	.color {
		height: 100%;
		aspect-ratio: 1/1;
		border-radius: 50%;
	}
</style>
