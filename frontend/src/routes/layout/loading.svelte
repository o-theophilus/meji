<script>
	import { scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { loading } from '$lib/store.js';
</script>

{#if $loading}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<div class="circle" />
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

		width: 200px;
		height: fit-content;
		padding: var(--sp2);
		border-radius: var(--sp1);

		text-align: center;
		color: var(--ac1);
		background-color: var(--ac6);
		box-shadow: var(--shad1);
	}

	.circle {
		--size: 50px;

		width: var(--size);
		height: var(--size);

		background-image: url('/image/loading.png');
		background-size: contain;
		background-repeat: no-repeat;

		animation: rotation 1s infinite linear;
	}

	@keyframes rotation {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(359deg);
		}
	}
</style>
