<script>
	let { value, active = false, small = false, onclick } = $props();

	let v = value.split(':');
	let label = v[0];
	let color = v[1];
</script>

<!-- TODO: make better and inline style -->




{#if label}
	<button class:active class:small class:onclick {onclick}>
		{label}

		{#if color}
			<div class="color block" style:background-color={color}></div>
		{/if}
	</button>
{:else}
	<button
		class:active
		class:small
		class:onclick
		style:background-color={color}
		{onclick}
	>
		<!-- {label} -->
	</button>
{/if}

<style>
	button {
		/* all: unset; */
		
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
		
		/* font-weight: 800; */
		
		background-color: transparent;
		border: 1px solid var(--ft2);
		color: var(--ft2);
		outline: 2px solid transparent;
		outline-offset: 1px;
		/* line-height: 100%; */
		
		&.active {
			outline-color: var(--ft1);
			/* border-color: transparent; */
		}
		&.onclick {
			cursor: pointer;
		}
		
		& .color {
			--size: 24px;
			height: var(--size);
			width: var(--size);
			border-radius: 4px;
			flex-shrink: 0;
		}

		&.small {
			--size: 24px;
			font-size: 0.8rem;
			/* padding: 2px; */
			/* padding: 0; */
			
			& .color {
				--size: 8px;
			}
		}
	}




</style>
