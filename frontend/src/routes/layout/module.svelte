<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
</script>

{#if $module}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="pos">
				<Button
					class="round hover_red small"
					on:keypress
					on:click={() => {
						$module = '';
					}}
				>
					<SVG type="close" size="12" />
				</Button>
			</div>

			<div class="content">
				<svelte:component this={$module.module} />
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		position: fixed;
		inset: 0;

		display: grid;
		align-items: center;
		justify-content: center;

		padding: calc(var(--sp3) * 2) var(--sp3);
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.block {
		position: relative;
		margin: auto;
	}

	.pos {
		position: absolute;
		top: -10px;
		right: -10px;
	}

	.content {
		/* width: 100%; */
		max-width: 500px;
		border-radius: var(--sp0);
		overflow: hidden;
		box-shadow: var(--shad1);
	}
</style>
