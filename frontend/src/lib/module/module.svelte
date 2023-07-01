<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module } from '$lib/store.js';
	import Button from '$lib/comp/button.svelte';
</script>

{#if $module}
	<section>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div
				class="close"
				on:keypress
				on:click={() => {
					$module = '';
				}}
			>
				<Button
					icon="close"
					icon_size="12"
					class="hover_red"
					on:keypress
					on:click={() => {
						$module = '';
					}}
				/>
			</div>
			<div class="content">
				<svelte:component this={$module.module} />
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		display: grid;
		align-items: center;
		justify-content: center;

		position: fixed;
		inset: 0;

		padding: calc(var(--gap3) * 2) var(--gap3);
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.block {
		position: relative;
	}

	.close {
		position: absolute;
		top: -10px;
		right: -10px;
	}

	.content {
		box-shadow: var(--shad1);
		border-radius: var(--brad1);
		overflow: hidden;
		width: 100%;
	}
</style>
