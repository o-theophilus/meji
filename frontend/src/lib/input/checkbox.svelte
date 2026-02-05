<script>
	import { Icon } from '$lib/macro';
	let { label, value = $bindable(), onclick } = $props();
</script>

<button {onclick}>
	<div class="checkbox" class:active={value}>
		<div class="icon">
			<Icon icon="check"></Icon>
		</div>
	</div>
	{label}
</button>

<style>
	button {
		all: unset;
		cursor: pointer;

		display: flex;
		align-items: center;
		gap: var(--checkbox-gap, 16px);
		font-size: var(--checkbox-font-size, 0.8rem);
		width: max-content;

		&:hover .checkbox {
			outline-color: var(--ft1);
		}
	}

	.checkbox {
		--size: 20px;
		position: relative;

		width: var(--size);
		height: var(--size);
		border-radius: 4px;
		outline: 2px solid var(--input);
		outline-offset: -2px;

		background-color: var(--input);
		cursor: pointer;

		transition: background-color 0.2s ease-in-out;

		&.active {
			background-color: var(--cl1);
		}
	}

	.icon {
		position: absolute;
		inset: 0;

		display: flex;
		align-items: center;
		justify-content: center;
		color: transparent;

		transition: color 0.2s ease-in-out;
	}
	.active .icon {
		color: white;
	}
</style>
