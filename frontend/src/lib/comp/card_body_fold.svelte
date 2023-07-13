<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
</script>

<div transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
	<slot>No Item</slot>
</div>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		width: 100%;

		color: var(--ac1);

		padding: var(--sp2);
		/* border-top: 2px solid var(--ac5); */
	}
</style>
