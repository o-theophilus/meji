<script>
	import { notify } from '$lib/store.svelte.js';
	import { fade } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { flip } from 'svelte/animate';

	import Item from './notify.one.svelte';
</script>

<section>
	{#each notify.value as one (one.key)}
		<div
			class="one"
			transition:fade={{ delay: 0, duration: 250, easing: cubicInOut }}
			animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}
		>
			<Item {one} />
		</div>
	{/each}
</section>

<style>
	section {
		z-index: 1;

		position: fixed;
		top: var(--headerHeight);
		right: 0;

		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 8px;

		pointer-events: none;
	}
</style>
