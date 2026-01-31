<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module } from '$lib/store.svelte.js';
	import { RoundButton } from '$lib/button';
</script>

{#if module.module}
	<section>
		<div></div>

		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div class="close">
				<RoundButton
					icon="x"
					onclick={() => {
						module.close();
					}}
				></RoundButton>
			</div>
			<div class="content">
				<svelte:component this={module.module} />
			</div>
		</div>

		<div></div>
	</section>
{/if}

<style>
	section {
		z-index: 1;

		display: grid;
		align-items: center;
		grid-template-columns: 1fr min(400px, 100%) 1fr;

		position: fixed;
		inset: 0;

		padding: 64px 24px;
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.close {
		position: absolute;
		--pos: -10px;
		top: var(--pos);
		right: var(--pos);

		--button-color: hsl(0, 0%, 70%);
		--button-color-hover_: hsl(0, 0%, 95%);
		--button-background-color_: darkred;
		--button-background-color-hover_: red;
		--button-outline-color-hover_: transparent;
	}

	.block {
		position: relative;
	}
	.content {
		background-color: var(--bg);
		box-shadow: 0 0 10px 0 var(--input);
		border-radius: 8px;

		overflow: hidden;
	}
</style>
