<script>
	let { value, active = false, small = false, onclick } = $props();

	let v = value.split(':');
	let label = v[0];
	let color = v[1];
</script>

{#if color && label}
	<button class:active class:small class:onclick class="block" {onclick}>
		{label}
		<div class="color block" style:background-color={color}></div>
	</button>
{:else}
	<button
		class:active
		class:small
		class:onclick
		class="block"
		style:background-color={color}
		{onclick}
	>
		{label}
	</button>
{/if}

<style>
	.block {
		--size: 40px;
		padding: 8px;

		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 8px;

		height: var(--size);
		min-width: var(--size);
		border-radius: 8px;
		border: none;

		font-weight: 800;

		background-color: var(--input);
		color: var(--ft2);
		outline: 2px solid var(--input);
		outline-offset: -2px;
	}

	.color {
		--size: 24px;
		border-radius: 4px;
	}

	.active {
		outline-color: var(--ft1);
	}

	.small {
		--size: 24px;
		font-size: 0.8rem;
	}
	.small .color {
		--size: 8px;
	}

	.onclick {
		cursor: pointer;
	}
</style>
