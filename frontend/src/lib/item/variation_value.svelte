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

	{#if v[0] && v[1]}
		<div class="gap" />
	{/if}

	{#if v[1]}
		<div class="color" style:background-color={v[1]} />
	{/if}
</button>

<style>
	button {
		display: inline-flex;
		align-items: center;

		border: none;

		background-color: transparent;
		border: 2px solid transparent;
		color: var(--ac2);
	}

	.gap {
		margin-left: var(--sp0);
	}
	.color {
		height: 16px;
		aspect-ratio: 1/1;
		border-radius: 50%;
		border: 2px solid var(--ac4);
	}

	.button {
		justify-content: center;
		cursor: pointer;

		height: 40px;
		min-width: 40px;
		padding: var(--sp1);
		border-radius: 20px;
		background-color: var(--ac5);
	}
	.button .color {
		height: 20px;
	}
	.button:hover {
		border-color: var(--ac4);
	}
	.button.active {
		border-color: var(--cl1);
	}
</style>
