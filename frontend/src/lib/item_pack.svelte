<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	export let style = 'grid';
	export let open = true;
</script>

{#if open}
	<div class={style} transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<slot {style} />
	</div>
{/if}

<style>
	.grid {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: repeat(2, 1fr);
	}

	@media screen and (min-width: 700px) {
		.grid {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 1000px) {
		.grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.list {
		display: grid;
		gap: var(--sp2);
	}

	.line {
		display: flex;
		gap: var(--sp1);
		overflow-x: auto;
		padding: var(--sp1);
	}
</style>
