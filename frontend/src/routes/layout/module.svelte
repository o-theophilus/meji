<script>
	import { scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import { module } from '$lib/store.js';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';
</script>

{#if $module}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<div class="content">
				<div class="close">
					<Button
						class="round hover_red"
						on:keypress
						on:click={() => {
							$module = '';
						}}
					>
						<SVG type="close" size="8" />
					</Button>
				</div>

				<svelte:component this={$module.module} />
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		position: fixed;
		inset: 0;
		z-index: 1;

		display: grid;

		padding: calc(var(--sp3) * 2) var(--sp3);
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.block {
		margin: auto;

		width: 100%;
	}

	.content {
		position: relative;

		max-width: 500px;
		margin: auto;
		border-radius: var(--sp0);
		overflow: hidden;
		box-shadow: var(--shad1);
	}

	.close {
		position: absolute;
		top: 2px;
		right: 2px;
	}
</style>
