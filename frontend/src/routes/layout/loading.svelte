<script>
	import { scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { loading } from '$lib/store.js';

	import Spinner from '$lib/loading_spinner.svelte';
</script>

{#if $loading}
	<section>
		<div
			class="block"
			class:string={typeof $loading == 'string'}
			transition:scale|local={{ delay: 0, duration: 200, easing: cubicInOut }}
		>
			<Spinner active />
			{#if typeof $loading == 'string'}
				{$loading}
			{/if}
		</div>
	</section>
{/if}

<style>
	section {
		display: flex;
		justify-content: center;

		position: fixed;
		inset: 0;
		z-index: 1;

		padding: var(--sp2);
	}

	.block {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp2);

		width: fit-content;
		height: fit-content;
		padding: var(--sp2);
		border-radius: var(--sp1);

		text-align: center;
		color: var(--ac1);
		background-color: var(--ac6);
		box-shadow: var(--shad1);
		outline: 2px solid var(--ac5);
	}
	.string {
		width: 200px;
	}
</style>
