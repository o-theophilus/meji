<script>
	let { value, active = false, onclick } = $props();

	let v = value.split(':');
	let label = v[0];
	let color = v[1];
</script>

<button class:active class:onclick {onclick}>
	{#if label}
		<span class="label">
			{label}
		</span>
	{/if}

	{#if color}
		<div class="color block" style:background-color={color}></div>
	{/if}
</button>

<style>
	button {
		all: unset;

		--size: 40px;
		--pad: 8px;

		display: inline-flex;
		align-items: center;
		justify-content: center;

		height: var(--size);
		min-width: var(--size);
		border-radius: 8px;
		border: none;

		background-color: transparent;
		border: 1px solid rgba(128, 128, 128, 0.3);
		color: var(--ft2);
		outline: 4px solid transparent;
		outline-offset: -4px;

		overflow: hidden;

		&.active {
			outline-color: var(--ft1);
		}
		&.onclick {
			cursor: pointer;
		}

		& .label {
			line-height: 100%;
		}

		& .color {
			height: var(--size);
			width: var(--size);
			border-radius: 4px;
			flex-shrink: 0;
		}

		&:has(.label) {
			gap: 8px;
			padding: 0 var(--pad);

			& .color {
				height: calc(var(--size) - var(--pad) * 2);
				width: calc(var(--size) - var(--pad) * 2);
				border: 1px solid rgba(128, 128, 128, 0.3);
			}
		}
	}
</style>
